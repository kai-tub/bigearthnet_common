"""
BigEarthNet Base Functions:

A collection of common functions that are frequently used when working with BigEarthNet.
"""

import bz2
import csv
import functools
import json
import warnings
from datetime import datetime
from enum import Enum
from importlib import resources
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Union

import appdirs
import dateutil
import fastcore.all as fc
import rich
import typer
from fastcore.basics import compose
from fastcore.dispatch import typedispatch
from pydantic import DirectoryPath, FilePath, validate_arguments

# from importlib_resources import files
from rich.table import Table

import bigearthnet_common
import bigearthnet_common.constants as ben_constants


class Resource(str, Enum):
    patches_with_cloud_and_snow = "patches_with_cloud_and_shadow.csv.bz2"
    patches_with_seasonal_snow = "patches_with_seasonal_snow.csv.bz2"
    patches_with_no_19_class_targets = "patches_with_no_19_class_targets.csv.bz2"
    s1_s2_mapping = "s1_s2_name_country_season.csv.bz2"
    country = "s1_s2_name_country_season.csv.bz2"
    season = "s1_s2_name_country_season.csv.bz2"
    test_csv = "test.csv.bz2"
    train_csv = "train.csv.bz2"
    val_csv = "val.csv.bz2"

    def __str__(self):
        return self.value


USER_DIR = Path(appdirs.user_data_dir("bigearthnet"))
USER_DIR.mkdir(exist_ok=True, parents=True)
PATCHES_WITH_SNOW_URL = (
    "http://bigearth.net/static/documents/patches_with_seasonal_snow.csv"
)
PATCHES_WITH_CLOUD_AND_SHADOW_URL = (
    "http://bigearth.net/static/documents/get_patches_with_cloud_and_shadow.csv"
)


def parse_datetime(inp: Union[str, datetime]) -> datetime:
    """
    Parses an input into a `datetime` object.
    Will try its best to infer the correct format from a string.
    If a `datetime` object is already provided it will be returned.
    Otherwise it will raise an error.
    """
    return _parse_datetime(inp)


@typedispatch
def _parse_datetime(acquisition_date: str) -> datetime:
    return compose(dateutil.parser.parse, _parse_datetime)(acquisition_date)


@typedispatch
def _parse_datetime(acquisition_date: datetime) -> datetime:
    return acquisition_date


@typedispatch
def _parse_datetime(acquisition_date: object) -> None:
    raise TypeError("Could not parse acquisition_date!")


@validate_arguments
def _read_json(
    json_fp: FilePath, expected_keys: Set, read_only_expected: bool = True
) -> Dict[str, str]:
    """
    Parse the json file given with the file path `json_fp`.
    The function checks if all of the `expected_keys` are present, which
    ensures that no keys have been accidentilly deleted (this has happend before).
    If `read_only_expected` is set, only the keys provided in `expected_keys` are read
    and returned.
    This prevents accidental processing of injected metadata.

    Args:
        json_fp (FilePath): Path to json file
        expected_keys (Set): Keys that are expected to be present in the json file
        read_only_expected (bool, optional): Read only the keys given in `expected_keys`. Defaults to True.

    Returns:
        [Dict[str, str]]: A dictionary of the keys.
    """
    try:
        complete_data = json.loads(json_fp.read_text())
    except json.JSONDecodeError:
        raise ValueError(f"Error trying to read json from: ", json_fp)

    missing_elements = expected_keys - complete_data.keys()
    if len(missing_elements) > 0:
        raise ValueError(f"{json_fp} is missing entries!", missing_elements)

    # ensure that the original values are loaded, as some users may customize the original json files
    if read_only_expected:
        return {k: v for k, v in complete_data.items() if k in expected_keys}
    return complete_data


def read_S1_json(json_fp: FilePath) -> Dict[str, str]:
    """
    A helper function that *safely* reads a BigEarthNet-S1 json file.
    It will ensure that all expected entries are present and only read those
    entries.
    This helps to avoid issues where the JSON files were accidentally modified
    or partially deleted.

    Note: This function will also silently fix a typo present in the `coordinates` key
    from version: S1_v1.0. A coordinates key is named `lly` and it should be `lry`.
    """
    data = _read_json(json_fp, ben_constants.BEN_S1_V1_0_JSON_KEYS)
    # Silently fix key error in S1
    if "lly" in data["coordinates"]:
        data["coordinates"]["lry"] = data["coordinates"].pop("lly")
    return data


def read_S2_json(json_fp: FilePath) -> Dict[str, str]:
    """
    A helper function that *safely* reads a BigEarthNet-S2 json file.
    It will ensure that all expected entries are present and only read those
    entries.
    This helps to avoid issues where the JSON files were accidentally modified
    or partially deleted.
    """
    return _read_json(json_fp, ben_constants.BEN_S2_V1_0_JSON_KEYS)


@validate_arguments
def get_s2_patch_directories(dir_path: DirectoryPath) -> List[Path]:
    """
    Will find all S2 patch directories in the provided `dir_path`.
    Only directories that strictly cohere to the naming convention will be returned.
    """
    return [
        p
        for p in dir_path.iterdir()
        if ben_constants.BEN_S2_RE.fullmatch(p.name) is not None
    ]


@validate_arguments
def get_s1_patch_directories(dir_path: DirectoryPath) -> List[Path]:
    """
    Will find all S1 patch directories in the provided `dir_path`.
    Only directories that strictly cohere to the naming convention will be returned.
    """
    return [
        p
        for p in dir_path.iterdir()
        if ben_constants.BEN_S1_RE.fullmatch(p.name) is not None
    ]


@functools.lru_cache()
def _conv_header_col_bz2_csv_resource_to_dict(
    resource, key_column: str, value_column: str
) -> Dict[str, str]:
    """
    Load a dictionary with the provided `key_column` and `value_column` after uncompressing
    the `bz2` compressed `resource` csv file.
    """
    # assert False, files(bigearthnet_common) / ""
    if not resources.is_resource(bigearthnet_common, resource):
        raise ValueError(
            f"{resource} resource is not available! This means that it was forgotten to be packaged."
        )

    with resources.path(bigearthnet_common, resource) as resource_path:
        with bz2.open(resource_path, mode="rt") as csv_file:
            reader = csv.DictReader(
                csv_file
            )  # field-names are encoded as first csv row
            if key_column not in reader.fieldnames:
                raise ValueError(
                    f"Key {key_column} is unkown! Resource provides: {reader.fieldnames}"
                )
            if value_column not in reader.fieldnames:
                raise ValueError(
                    f"Value {value_column} is unkown! Resource provides: {reader.fieldnames}"
                )
            return {row[key_column]: row[value_column] for row in reader}


# FUTURE: Could merge the underlying logic together
@functools.lru_cache()
def _conv_header_col_bz2_csv_resource_to_set(resource, key_column: str) -> Set[str]:
    """
    Load a dictionary with the provided `key_column` after uncompressing
    the `bz2` compressed `resource` csv file.
    """
    print(resource)
    if not resources.is_resource(bigearthnet_common, resource):
        # if not files(bigearthnet_common) / resource:
        raise ValueError(
            f"{resource} resource is not available! This means that it was forgotten to be packaged."
        )

    with resources.path(bigearthnet_common, resource) as resource_path:
        with bz2.open(resource_path, mode="rt") as csv_file:
            reader = csv.DictReader(
                csv_file
            )  # field-names are encoded as first csv row
            if key_column not in reader.fieldnames:
                raise ValueError(
                    f"Key {key_column} is unkown! Resource provides: {reader.fieldnames}"
                )
            return {row[key_column] for row in reader}


def get_all_s2_patch_names() -> Set[str]:
    resource = Resource.s1_s2_mapping
    return _conv_header_col_bz2_csv_resource_to_set(resource, "s2_name")


def get_all_s1_patch_names() -> Set[str]:
    resource = Resource.s1_s2_mapping
    return _conv_header_col_bz2_csv_resource_to_set(resource, "s1_name")


def _load_s1_s2_patch_name_mapping(from_s1_to_s2: bool = True) -> Dict[str, str]:
    """
    Load a dictionary which maps the S1 patch name to the S2 patch name (if `from_s1_to_s2`) or
    the S2 patch name to the S1 patch name.

    The compressed data could be regenerated with (requires the output of `bigearthnet_gdf_builder`):

    >>> import geopandas
    >>> raw_gdf = geopandas.read_parquet("raw_ben_s1_gdf.parquet")
    >>> raw_gdf = raw_gdf.rename({"name": "s1_name", "corresponding_s2_patch": "s2_name"}, axis=1)
    >>> raw_gdf.to_csv("s1_s2_mapping.csv.bz2", columns=["s1_name", "s2_name"], index=False)
    """
    resource = Resource.s1_s2_mapping
    key, value = ("s1_name", "s2_name") if from_s1_to_s2 else ("s2_name", "s1_name")
    return _conv_header_col_bz2_csv_resource_to_dict(resource, key, value)


def get_complete_s1_to_s2_patch_name_mapping() -> Dict[str, str]:
    """
    Load entire Sentinel-1 to Sentinel-2 BigEarthNet patch name mapping.

    Returns:
        Dict[str, str]: Sentinel-1 patch name keys with corresponding Sentinel-2 patch name as value
    """
    return _load_s1_s2_patch_name_mapping(from_s1_to_s2=True)


def get_complete_s2_to_s1_patch_name_mapping() -> Dict[str, str]:
    """
    Load entire Sentinel-2 to Sentinel-1 BigEarthNet patch name mapping.

    Returns:
        Dict[str, str]: Sentinel-2 patch name keys with corresponding Sentinel-1 patch name as value
    """
    return _load_s1_s2_patch_name_mapping(from_s1_to_s2=False)


def s1_to_s2_patch_name(s1_patch_name: str) -> str:
    """
    Convert BigEarthNet Sentinel-1 patch name to Sentinel-2 patch name.
    The function caches intermediate results.
    The function should be highly performant.

    Args:
        s1_patch_name (str): complete BigEarthNet Sentinel-1 patch name

    Returns:
        str: Corresponding Sentinel-2 patch name
    """
    return get_complete_s1_to_s2_patch_name_mapping()[s1_patch_name]


def s2_to_s1_patch_name(s2_patch_name: str) -> str:
    """
    Convert BigEarthNet Sentinel-2 patch name to Sentinel-1 patch name.
    The function caches intermediate results.
    The function should be highly performant.

    Args:
        s2_patch_name (str): complete BigEarthNet Sentinel-2 patch name

    Returns:
        str: Corresponding Sentinel-1 patch name
    """
    return get_complete_s2_to_s1_patch_name_mapping()[s2_patch_name]


def get_patches_to_country_mapping(use_s2_patch_names: bool = True) -> Dict[str, str]:
    """
    Return a dictionary that maps a patch name to a country.
    If `use_s2_patch_names` is set, use the BigEarthNet Sentinel-2 patch names.
    Otherwise, use the Sentinel-1 patch names.

    The compressed data could be regenerated with (requires the output of `bigearthnet_gdf_builder`):

    >>> import geopandas
    >>> extended_gdf = geopandas.read_parquet("extended_ben_s1_gdf.parquet")
    >>> extended_gdf = raw_gdf.rename({"name": "s1_name", "corresponding_s2_patch": "s2_name"}, axis=1)
    >>> extended_gdf.to_csv("country.csv.bz2", columns=["s1_name", "s2_name", "country"], index=False)
    """
    resource = Resource.country
    key = "s2_name" if use_s2_patch_names else "s1_name"
    return _conv_header_col_bz2_csv_resource_to_dict(resource, key, "country")


@validate_arguments
def is_s2_patch(patch_name: str) -> bool:
    """Quick regex check if name is a valid S2 patch name"""
    return ben_constants.BEN_S2_RE.fullmatch(patch_name)


@validate_arguments
def is_s1_patch(patch_name: str) -> bool:
    """Quick regex check if name is a valid S2 patch name"""
    return ben_constants.BEN_S1_RE.fullmatch(patch_name)


def get_country_from_patch_name(patch_name: str) -> str:
    """
    Fast function that returns the country to which the patch `patch_name` belongs to.

    This works for S1 and S2 patch names!
    """
    if is_s2_patch(patch_name):
        return get_patches_to_country_mapping(use_s2_patch_names=True)[patch_name]
    return get_patches_to_country_mapping(use_s2_patch_names=False)[patch_name]


def get_patches_to_season_mapping(use_s2_patch_names: bool = True) -> Dict[str, str]:
    """
    Return a dictionary that maps a patch name to the season of the acquisition date.
    If `use_s2_patch_names` is set, use the BigEarthNet Sentinel-2 patch names.
    Otherwise, use the Sentinel-1 patch names.

    The compressed data could be regenerated with (requires the output of `bigearthnet_gdf_builder`):

    >>> import geopandas
    >>> extended_gdf = geopandas.read_parquet("extended_ben_s1_gdf.parquet")
    >>> extended_gdf = raw_gdf.rename({"name": "s1_name", "corresponding_s2_patch": "s2_name"}, axis=1)
    >>> extended_gdf.to_csv("season.csv.bz2", columns=["s1_name", "s2_name", "season"], index=False)
    """
    resource = Resource.season
    key = "s2_name" if use_s2_patch_names else "s1_name"
    return _conv_header_col_bz2_csv_resource_to_dict(resource, key, "season")


def get_season_from_patch_name(patch_name: str) -> str:
    """
    Fast function that returns the season in which the patch `patch_name` was sensed.

    This works for S1 and S2 patch names!
    """
    if is_s2_patch(patch_name):
        return get_patches_to_season_mapping(use_s2_patch_names=True)[patch_name]
    return get_patches_to_season_mapping(use_s2_patch_names=False)[patch_name]


@validate_arguments
def _conv_single_col_csv_resource_to_set(
    resource: str,
) -> Set[str]:
    """
    Given a `resource` name of an encoded CSV file *without* a header
    line and only a single column, return the set of
    all values.
    """
    if not resources.is_resource(bigearthnet_common, resource):
        raise ValueError(f"{resource} is an unknown resource!")

    with resources.path(bigearthnet_common, resource) as resource_path:
        with bz2.open(resource_path, mode="rt") as csv_file:
            col_name = "Column"
            reader = csv.DictReader(csv_file, fieldnames=[col_name])
            return {row[col_name] for row in reader}


@functools.lru_cache()
def get_s2_patches_with_seasonal_snow() -> Set[str]:
    """List all patches with seasonal snow from **original** BigEarthNet-S2 dataset."""
    return _conv_single_col_csv_resource_to_set(Resource.patches_with_seasonal_snow)


@functools.lru_cache()
def get_s2_patches_with_cloud_and_shadow() -> Set[str]:
    """List all patches with cloud and shadow from **original** BigEarthNet-S2 dataset."""
    return _conv_single_col_csv_resource_to_set(Resource.patches_with_cloud_and_snow)


@functools.lru_cache()
def get_s1_patches_with_seasonal_snow() -> Set[str]:
    """List all patches with seasonal snow from **original** BigEarthNet-S1 dataset."""
    _s2_patches_with_snow = get_s2_patches_with_seasonal_snow()
    return {s2_to_s1_patch_name(s2_patch) for s2_patch in _s2_patches_with_snow}


@functools.lru_cache()
def get_s1_patches_with_cloud_and_shadow() -> Set[str]:
    """List all patches with cloud and shadow from **original** BigEarthNet-S1 dataset."""
    _s2_patches_with_clouds = get_s2_patches_with_cloud_and_shadow()
    return {s2_to_s1_patch_name(s2_patch) for s2_patch in _s2_patches_with_clouds}


@validate_arguments
def is_snowy_patch(patch_name: str):
    """
    Fast function that checks whether `patch_name` is a patch
    that contains a lot of seasonal snow.

    This works for S1 and S2 patch names!
    """
    return (
        patch_name in get_s2_patches_with_seasonal_snow()
        or patch_name in get_s1_patches_with_seasonal_snow()
    )


@validate_arguments
def is_cloudy_shadowy_patch(patch_name: str):
    """
    Fast function that checks whether `patch_name` is a patch
    that contains a lot of shadow or is obstructed by clouds.

    This works for S1 and S2 patch names!
    """
    return (
        patch_name in get_s2_patches_with_cloud_and_shadow()
        or patch_name in get_s1_patches_with_cloud_and_shadow()
    )


@functools.lru_cache()
def get_s2_patches_with_no_19_class_target() -> Set[str]:
    """
    List all patches from the BigEarthNet-S2 dataset that
    have _no_ defined classes with the 19-class nomenclature.

    Note: This set still includes patches with snow, clouds, or shadows.

    To re-build the file, it is necessary to use the output of `bigearthnet_gdf_builder`:

    >>> raw_gdf = geopandas.read_parquet("raw_ben_s2_gdf.parquet")
    >>> raw_gdf["new_labels"] = raw_gdf["labels"].apply(old2new_labels)
    >>> no_19_label_targets = raw_gdf[raw_gdf["new_labels"].isna()]
    >>> no_19_label_targets.to_csv("patches_with_no_19_class_targets.csv.bz2", columns=["name"], index=False, header=False)
    """
    return _conv_single_col_csv_resource_to_set(
        Resource.patches_with_no_19_class_targets
    )


@functools.lru_cache()
def get_s1_patches_with_no_19_class_target() -> Set[str]:
    """
    List all patches from the BigEarthNet-S1 dataset that
    have _no_ defined classes with the 19-class nomenclature.

    Note: This set still includes patches with snow, clouds, or shadows.

    The patch names are converted from `get_s2patches_with_no_19_class_targets`
    for compactness.
    """
    s2_patches_no_19_classes = _conv_single_col_csv_resource_to_set(
        Resource.patches_with_no_19_class_targets
    )
    return {s2_to_s1_patch_name(s2_patch) for s2_patch in s2_patches_no_19_classes}


@validate_arguments
def has_19_class_target(patch_name: str) -> bool:
    """
    Fast function that checks whether `patch_name` is a patch
    that has at least a single 19-class target label.

    This works for S1 and S2 patch names!
    """
    return not (
        patch_name in get_s1_patches_with_no_19_class_target()
        or patch_name in get_s2_patches_with_no_19_class_target()
    )


# FUTURE: Remove this bz2 file and repackage it inside of the
# metadata collection file
# "https://git.tu-berlin.de/rsim/BigEarthNet-S2_19-classes_models/-/raw/master/splits/train.csv",
@functools.lru_cache()
def get_s2_patches_from_original_train_split() -> Set[str]:
    """
    List all Sentinel-2 train patches from the original train/validation/test split.
    """
    return _conv_single_col_csv_resource_to_set(Resource.train_csv)


@functools.lru_cache()
def get_s1_patches_from_original_train_split() -> Set[str]:
    """
    List all Sentinel-1 train patches from the original train/validation/test split.
    """
    s2_train_patches = get_s2_patches_from_original_train_split()
    return {s2_to_s1_patch_name(s2_patch) for s2_patch in s2_train_patches}


@functools.lru_cache()
def get_s2_patches_from_original_validation_split() -> Set[str]:
    """
    List all Sentinel-2 validation patches from the original train/validation/test split.
    """
    return _conv_single_col_csv_resource_to_set(Resource.val_csv)


@functools.lru_cache()
def get_s1_patches_from_original_validation_split() -> Set[str]:
    """
    List all Sentinel-1 validation patches from the original train/validation/test split.
    """
    s2_validation_patches = get_s2_patches_from_original_validation_split()
    return {s2_to_s1_patch_name(s2_patch) for s2_patch in s2_validation_patches}


@functools.lru_cache()
def get_s2_patches_from_original_test_split() -> Set[str]:
    """
    List all Sentinel-2 test patches from the original train/validation/test split.
    """
    return _conv_single_col_csv_resource_to_set(Resource.test_csv)


@functools.lru_cache()
def get_s1_patches_from_original_test_split() -> Set[str]:
    """
    List all Sentinel-1 test patches from the original train/validation/test split.
    """
    s2_test_patches = get_s2_patches_from_original_test_split()
    return {s2_to_s1_patch_name(s2_patch) for s2_patch in s2_test_patches}


@validate_arguments
def get_original_split_from_patch_name(patch: str) -> Optional[str]:
    """
    Returns "train"/"validation"/"test" or `None`.
    The value is retrieved from the original BigEarthNet-S1/S2
    train/validation/test split. If the input is not present
    in any split, it will return `None` and raise a UserWarning.
    This happens for patches that are either in the
    cloud/shadow or seasonal snow set or if there exists no 19-label target.

    Note: This works for Sentinel-2 and Sentinel-1 patch names!
    """
    s1_train = get_s1_patches_from_original_train_split()
    s2_train = get_s2_patches_from_original_train_split()
    s1_validation = get_s1_patches_from_original_validation_split()
    s2_validation = get_s2_patches_from_original_validation_split()
    s1_test = get_s1_patches_from_original_test_split()
    s2_test = get_s2_patches_from_original_test_split()

    if patch in s1_train or patch in s2_train:
        return ben_constants.Split.train
    elif patch in s1_validation or patch in s2_validation:
        return ben_constants.Split.validation
    elif patch in s1_test or patch in s2_test:
        return ben_constants.Split.test
    warnings.warn(
        "Provided an input patch name which was not part of the original split.",
        UserWarning,
    )
    return None


@validate_arguments
def _old2new_label(old_label: str) -> Optional[str]:
    """
    Converts old-style BigEearthNet label to the
    new labels.

    > Note: Some labels were removed! This function
    will return `None` if the label was removed and
    raise a `KeyError` if the input label is unknown.
    """
    return ben_constants.OLD2NEW_LABELS_DICT[old_label]


def old2new_labels(old_labels: Iterable[str]) -> Optional[List[str]]:
    """
    Converts a list of old-style BigEarthNet labels
    to a list of labels.

    If there are no corresponding new labels (which can happen with original BEN patches!)
    then the function will return `None` and raise a user warning.

    If an illegal/unknown input label is provided, a `KeyError` is raised.
    """
    new_labels = [
        _old2new_label(l) for l in old_labels if _old2new_label(l) is not None
    ]
    if len(old_labels) > 0 and len(new_labels) == 0:
        warnings.warn(
            "Provided a list of old labels that only contains `removed` labels!",
            UserWarning,
        )
        new_labels = None
    return new_labels


@validate_arguments
def ben_19_labels_to_multi_hot(
    labels: Iterable[str], lex_sorted: bool = True
) -> List[float]:
    """
    Convenience function that converts an input iterable of labels into
    a multi-hot encoded vector.
    If `lex_sorted` is True (default) the classes are lexigraphically ordered, as they are
    in `constants.NEW_LABELS`.
    If `lex_sorted` is False, the original order from the BigEarthNet paper is used, as
    they are given in `constants.NEW_LABELS_ORIGINAL_ORDER`.

    If an unknown label is given, a `KeyError` is raised.

    Be aware that this approach assumes that **all** labels are actually used in the dataset!
    This is not necessarily the case if you are using a subset!
    For example, the "Agro-forestry areas" class is only present in Portugal and in no other country!
    """
    ordered_lbls = (
        ben_constants.NEW_LABELS
        if lex_sorted
        else ben_constants.NEW_LABELS_ORIGINAL_ORDER
    )
    lbls_to_idx = fc.L(ordered_lbls).val2idx()
    idxs = [lbls_to_idx[label] for label in labels]
    multi_hot = fc.L([0] * len(ben_constants.NEW_LABELS))
    multi_hot[idxs] = 1.0
    return list(multi_hot)


@validate_arguments
def ben_43_labels_to_multi_hot(
    labels: Iterable[str], lex_sorted: bool = True
) -> List[float]:
    """
    Convenience function that converts an input iterable of labels into
    a multi-hot encoded vector.
    If `lex_sorted` is True (default) the classes are lexigraphically ordered, as they are
    in `constants.OLD_LABELS`.
    If `lex_sorted` is False, the original order from the BigEarthNet paper is used, as
    they are given in `constants.OLD_LABELS_ORIGINAL_ORDER`.

    If an unknown label is given, a `KeyError` is raised.

    Be aware that this approach assumes that **all** labels are actually used in the dataset!
    This is not necessarily the case if you are using a subset!
    For example, the "Agro-forestry areas" class is only present in Portugal and in no other country!
    """
    ordered_lbls = (
        ben_constants.OLD_LABELS
        if lex_sorted
        else ben_constants.OLD_LABELS_ORIGINAL_ORDER
    )
    lbls_to_idx = fc.L(ordered_lbls).val2idx()
    idxs = [lbls_to_idx[label] for label in labels]
    multi_hot = fc.L([0] * len(ben_constants.OLD_LABELS))
    multi_hot[idxs] = 1.0
    return list(multi_hot)


def _are_s1_files_complete(patch_path: DirectoryPath) -> bool:
    """
    Check if all S1-patch files exists (bands and json files) and are not empty.
    """
    file_suffixes = ["VV", "VH", "_labels_metadata.json"]
    for suffix in file_suffixes:
        file = patch_path / f"{patch_path.name}{suffix}"
        if not file.exists() or file.stat().st_size == 0:
            return False
    return True


def _are_s2_files_complete(patch_path: DirectoryPath) -> bool:
    """
    Check if all S2-patch files exists (bands and json files) and are not empty.
    """
    file_suffixes = [f"_B{i:02}.tif" for i in range(1, 13) if i != 10] + [
        "_B8A",
        "_labels_metadata.json",
    ]
    for suffix in file_suffixes:
        file = patch_path / f"{patch_path.name}{suffix}"
        if not file.exists() or file.stat().st_size == 0:
            return False
    return True


def _print_missing_dirs(missing_dirs, show_num: int = 10) -> None:
    rich.print("There are some missing directories!")
    rich.print(
        "The following directories are missing compared to the complete BEN archive."
    )
    show_num = min(show_num, len(missing_dirs))
    rich.print(
        f"Showing only the first {show_num} invalid directories of {len(missing_dirs)}"
    )
    rich.print([d for _, d in zip(range(show_num), missing_dirs)])


def _print_dirs_with_missing_files(dirs_with_missing_files, show_num: int = 10) -> None:
    rich.print("There are some invalid directories!")
    rich.print("The following directories are missing files.")
    show_num = min(show_num, len(dirs_with_missing_files))
    rich.print(
        f"Showing only the first {show_num} invalid directories of {len(dirs_with_missing_files)}"
    )
    rich.print([d for _, d in zip(range(show_num), dirs_with_missing_files)])


@validate_arguments
def _validate_ben_root_directory(
    dir_path: DirectoryPath, is_sentinel2: bool
) -> Set[str]:
    files = {f for f in dir_path.glob("*")}
    patch_names = get_all_s2_patch_names() if is_sentinel2 else get_all_s1_patch_names()
    expected_directories = {dir_path / patch for patch in patch_names}
    missing_directories = expected_directories - files
    ben_dirs = expected_directories & files
    completeness_checker = (
        _are_s2_files_complete if is_sentinel2 else _are_s1_files_complete
    )
    directories_with_missing_files = {
        f for f in ben_dirs if not completeness_checker(f)
    }
    if missing_directories == set() and directories_with_missing_files == set():
        rich.print("Nothing seems to be missing.")
        rich.print(f"The Sentinel directory {dir_path} looks complete.")
        return set()
    if missing_directories != set():
        _print_missing_dirs(missing_directories)
    if directories_with_missing_files != set():
        _print_dirs_with_missing_files(directories_with_missing_files)
    return missing_directories | directories_with_missing_files


def validate_ben_s2_root_directory(dir_path: Path) -> Set[str]:
    """
    Quickly check if all expected files from the BigEarthNet-S2 archive are present.

    This funtion will _not_ check if the files are correct or if they were modified!
    The function will perform a simple existence check and verify that each file is not empty.
    Other files will be ignored.
    """
    return _validate_ben_root_directory(dir_path, is_sentinel2=True)


def validate_ben_s1_root_directory(dir_path: Path) -> Set[str]:
    """
    Quickly check if all expected files from the BigEarthNet-S1 archive are present.

    This funtion will _not_ check if the files are correct or if they were modified!
    The function will perform a simple existence check and verify that each file is not empty.
    Other files will be ignored.
    """
    return _validate_ben_root_directory(dir_path, is_sentinel2=False)


def validate_ben_s2_root_directory_cli():
    app = typer.Typer()
    app.command()(validate_ben_s2_root_directory)
    app()


def validate_ben_s1_root_directory_cli():
    app = typer.Typer()
    app.command()(validate_ben_s1_root_directory)
    app()


@validate_arguments
def describe_patch(patch_names: List[str]) -> Table:
    """
    Given a list of patch names return a table that summarizes
    the metadata.
    """
    columns = [
        "Sentinel-1 Name",
        "Sentinel-2 Name",
        "Original Split",
        "Country",
        "Season",
        "Snowy",
        "Cloudy / Shadowy",
        "Valid 19-label",
    ]
    y = "✅"
    n = "❌"
    t = Table(
        title=f"Metadata Summary",
        caption=f"Patch(es): {patch_names}",
        expand=True,
        leading=1,
    )
    for c in columns:
        t.add_column(header=c, overflow="fold", justify="center")

    for patch_name in patch_names:
        if is_s1_patch(patch_name):
            s1_name = patch_name
            s2_name = s1_to_s2_patch_name(s1_name)
        elif is_s2_patch(patch_name):
            s2_name = patch_name
            s1_name = s2_to_s1_patch_name(s2_name)
        else:
            raise ValueError(f"Input: {patch_name} is not a valid S1/S2 patch name!")

        split = get_original_split_from_patch_name(s2_name)
        country = get_country_from_patch_name(s2_name)
        season = get_season_from_patch_name(s2_name)
        snowy = y if is_snowy_patch(s2_name) else n
        cloudy = y if is_cloudy_shadowy_patch(s2_name) else n
        valid_19 = y if has_19_class_target(s2_name) else n
        t.add_row(s1_name, s2_name, split, country, season, snowy, cloudy, valid_19)
    rich.print(t)
    return t


def describe_patch_cli():
    app = typer.Typer()
    app.command()(describe_patch)
    app()
