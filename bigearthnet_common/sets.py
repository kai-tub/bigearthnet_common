import csv
from pathlib import Path
from typing import List, Sequence, Set

import fastcore.all as fc
import natsort
import typer
from pydantic import validate_arguments

import bigearthnet_common.base as ben_base
import bigearthnet_common.constants as ben_constants


def get_all_s2_patches() -> Set[str]:
    """
    Returns a set of all S2 patch names.
    """
    return set(ben_base.get_complete_s2_to_s1_patch_name_mapping().keys())


def get_all_s1_patches() -> Set[str]:
    """
    Returns a set of all S1 patch names.
    """
    return set(ben_base.get_complete_s1_to_s2_patch_name_mapping().keys())


def get_recommended_s2_patches() -> Set[str]:
    s2_patches = get_all_s2_patches()
    no_19_class_targets = ben_base.get_s2_patches_with_no_19_class_target()
    recommended_s2_patches = {
        p
        for p in s2_patches
        if not ben_base.is_snowy_patch(p)
        and not ben_base.is_cloudy_shadowy_patch(p)
        and p not in no_19_class_targets
    }
    return recommended_s2_patches


def get_recommended_s1_patches() -> Set[str]:
    s1_patches = get_all_s1_patches()
    no_19_class_targets = ben_base.get_s1_patches_with_no_19_class_target()
    recommended_s1_patches = {
        p
        for p in s1_patches
        if not ben_base.is_snowy_patch(p)
        and not ben_base.is_cloudy_shadowy_patch(p)
        and p not in no_19_class_targets
    }
    return recommended_s1_patches


@validate_arguments
def filter_s2_patches_by_country(
    patches: Sequence, country: ben_constants.Country
) -> Set[str]:
    if country not in ben_constants.COUNTRIES:
        raise ValueError(
            f"{country} is not one of the BEN countries: {ben_constants.COUNTRIES}!"
        )

    patch_country_mapping = ben_base.get_patches_to_country_mapping(
        use_s2_patch_names=True
    )
    return {p for p in patches if patch_country_mapping[p] == country}


@validate_arguments
def filter_s1_patches_by_country(
    patches: Sequence, country: ben_constants.Country
) -> Set[str]:
    if country not in ben_constants.COUNTRIES:
        raise ValueError(
            f"{country} is not one of the BEN countries: {ben_constants.COUNTRIES}!"
        )

    patch_country_mapping = ben_base.get_patches_to_country_mapping(
        use_s2_patch_names=False
    )
    return {p for p in patches if patch_country_mapping[p] == country}


@validate_arguments
def filter_patches_by_country(
    sentinel_source: ben_constants.SentinelSource,
    patches: Sequence,
    country: ben_constants.Country,
):
    """
    Given Sentinel-1/2 named-patches, return only those patches that belong to a given
    country.
    """
    return (
        filter_s1_patches_by_country(patches, country)
        if sentinel_source == ben_constants.SentinelSource.S1
        else filter_s2_patches_by_country(patches, country)
    )


@validate_arguments
def filter_s2_patches_by_season(
    patches: Sequence, season: ben_constants.Season
) -> Set[str]:
    patch_season_mapping = ben_base.get_patches_to_season_mapping(
        use_s2_patch_names=True
    )
    return {p for p in patches if patch_season_mapping[p] == season}


@validate_arguments
def filter_s1_patches_by_season(
    patches: Sequence, season: ben_constants.Season
) -> Set[str]:
    patch_season_mapping = ben_base.get_patches_to_season_mapping(
        use_s2_patch_names=False
    )
    return {p for p in patches if patch_season_mapping[p] == season}


@validate_arguments
def filter_patches_by_season(
    sentinel_source: ben_constants.SentinelSource,
    patches: Sequence,
    season: ben_constants.Season,
):
    """
    Given Sentinel-1/2 named-patches, return only those patches that belong to a given
    season.
    """
    return (
        filter_s1_patches_by_season(patches, season)
        if sentinel_source == ben_constants.SentinelSource.S1
        else filter_s2_patches_by_season(patches, season)
    )


@validate_arguments
def filter_s1_patches_by_split(patches: Sequence, split: ben_constants.Split):
    get_split_func = {
        split.train: ben_base.get_s1_patches_from_original_train_split,
        split.validation: ben_base.get_s1_patches_from_original_validation_split,
        split.test: ben_base.get_s1_patches_from_original_test_split,
    }
    split_patches = get_split_func[split]()
    return patches & split_patches


@validate_arguments
def filter_s2_patches_by_split(patches: Sequence, split: ben_constants.Split):
    get_split_func = {
        split.train: ben_base.get_s2_patches_from_original_train_split,
        split.validation: ben_base.get_s2_patches_from_original_validation_split,
        split.test: ben_base.get_s2_patches_from_original_test_split,
    }
    split_patches = get_split_func[split]()
    return set(patches) & split_patches


@validate_arguments
def filter_patches_by_split(
    sentinel_source: ben_constants.SentinelSource,
    patches: Sequence,
    split: ben_constants.Split,
):
    """
    Given Sentinel-1/2 named-patches, return only those patches that belong to a given
    split.
    """
    return (
        filter_s1_patches_by_split(patches, split)
        if sentinel_source == ben_constants.SentinelSource.S1
        else filter_s2_patches_by_split(patches, split)
    )


@validate_arguments
def build_set(
    sentinel_source: ben_constants.SentinelSource,
    seasons: List[ben_constants.Season] = [s.value for s in ben_constants.Season],
    countries: List[ben_constants.Country] = [c.value for c in ben_constants.Country],
    remove_unrecommended_dl_patches: bool = True,
) -> Set[str]:
    """
    Create a subset of the Sentinel-1/Sentinel-2 patches.
    The returned list will be naturally sorted to produce
    deterministic results.
    """
    use_s1 = sentinel_source == ben_constants.SentinelSource.S1
    # FUTURE: could be split up into higher level functions
    if remove_unrecommended_dl_patches:
        patches = (
            get_recommended_s1_patches() if use_s1 else get_recommended_s2_patches()
        )
    else:
        patches = get_all_s1_patches() if use_s1 else get_all_s2_patches()

    if len(seasons) > 0:
        patches = {
            patch
            for season in seasons
            for patch in filter_patches_by_season(sentinel_source, patches, season)
        }
    if len(countries) > 0:
        patches = {
            patch
            for country in countries
            for patch in filter_patches_by_country(sentinel_source, patches, country)
        }
    return patches


@fc.delegates(build_set)
@validate_arguments
def build_csv_sets(
    file_path: Path,
    sentinel_source: ben_constants.SentinelSource,
    write_separate_splits: bool = True,
    **kwargs,
):
    """
    Build CSV files that contain Sentinel-1/2 patches names with the given restrictions.
    By default, the patches will be grouped by the orignal train/validation/test split.
    This is generally a good starting point, but not ideal for all use-cases.
    If `write_separate_splits` is `False`, the output will contain all patches.
    The generated file does **not** contain a header row, as this style was used in all the other
    publicly available BigEarthNet CSV files.

    The patch names will be naturally sorted to ensure deterministic outputs.
    """

    def _write_csv(fp, patches):
        sorted_patches = natsort.natsorted(patches)
        with open(fp.with_suffix(".csv"), "w") as csv_file:
            writer = csv.writer(csv_file)
            for patch in sorted_patches:
                writer.writerow([patch])

    patches = build_set(sentinel_source, **kwargs)
    if write_separate_splits:
        train_patches = filter_patches_by_split(
            sentinel_source, patches, ben_constants.Split.train
        )
        validation_patches = filter_patches_by_split(
            sentinel_source, patches, ben_constants.Split.validation
        )
        test_patches = filter_patches_by_split(
            sentinel_source, patches, ben_constants.Split.test
        )
        if min(len(train_patches), len(validation_patches), len(test_patches)) == 0:
            raise RuntimeError("One of the train/val/test splits is empty!")
        if (train_patches & validation_patches & test_patches) != set():
            raise RuntimeError(
                "There is an overlap between the train/validation/test patches!"
            )
        _write_csv(file_path.with_name(f"{file_path.name}_train.csv"), train_patches)
        _write_csv(
            file_path.with_name(f"{file_path.name}_validation.csv"), validation_patches
        )
        _write_csv(file_path.with_name(f"{file_path.name}_test.csv"), test_patches)
    else:
        _write_csv(file_path, patches)


def build_csv_sets_cli():
    app = typer.Typer(name="ben_build_csv_sets")
    app.command()(build_csv_sets)
    app()


if __name__ == "__main__" and not fc.IN_IPYTHON:
    build_csv_sets_cli()
