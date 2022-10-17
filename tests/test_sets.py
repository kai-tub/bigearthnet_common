from pathlib import Path

import pytest
from pydantic import ValidationError

import bigearthnet_common.constants as ben_constants
from bigearthnet_common.sets import *


def test_get_all_s1_patches():
    assert len(get_all_s1_patches()) == ben_constants.BEN_COMPLETE_SIZE


def test_get_all_s2_patches():
    assert len(get_all_s2_patches()) == ben_constants.BEN_COMPLETE_SIZE


def test_get_recommended_s1_patches():
    assert len(get_recommended_s1_patches()) == ben_constants.BEN_RECOMMENDED_SIZE


def test_get_recommended_s2_patches():
    assert len(get_recommended_s2_patches()) == ben_constants.BEN_RECOMMENDED_SIZE


def test_filter_patches_by_season_order():
    patch_season_mapping = ben_base.get_patches_to_season_mapping(
        use_s2_patch_names=True
    )
    winter_patches = [
        p for p, s in patch_season_mapping.items() if s == ben_constants.Season.Winter
    ]
    winter_patches = winter_patches[:10]
    assert len(winter_patches) > 1, "Broken test"

    # S2 tests
    out = filter_s2_patches_by_season(winter_patches, ben_constants.Season.Winter)
    # assert that the order remains the same
    assert winter_patches == out
    winter_patches = winter_patches[::-1]
    out = filter_s2_patches_by_season(winter_patches, ben_constants.Season.Winter)
    # assert that the order remains the same
    assert winter_patches == out

    # S1 tests
    s1_winter_patches = [ben_base.s2_to_s1_patch_name(p2) for p2 in winter_patches]
    out = filter_s1_patches_by_season(s1_winter_patches, ben_constants.Season.Winter)
    assert s1_winter_patches == out
    s1_winter_patches = s1_winter_patches[::-1]
    out = filter_s1_patches_by_season(s1_winter_patches, ben_constants.Season.Winter)
    # assert that the order remains the same
    assert s1_winter_patches == out


def test_filter_patches_by_country_order():
    patch_country_mapping = ben_base.get_patches_to_country_mapping(
        use_s2_patch_names=True
    )
    lithuania_patches = [
        p
        for p, c in patch_country_mapping.items()
        if c == ben_constants.Country.Lithuania
    ]
    lithuania_patches = lithuania_patches[:10]
    out = filter_s2_patches_by_country(
        lithuania_patches, ben_constants.Country.Lithuania
    )
    # assert that the order remains the same
    assert lithuania_patches == out
    lithuania_patches = lithuania_patches[::-1]
    out = filter_s2_patches_by_country(
        lithuania_patches, ben_constants.Country.Lithuania
    )
    # assert that the order remains the same
    assert lithuania_patches == out


def test_build_sets():
    assert len(build_set("S1", seasons=["Winter"])) < len(
        build_set("S2", seasons=["Winter", "Fall"])
    )
    assert len(build_set("S1", countries=["Austria"])) < len(
        build_set(
            "S2",
            countries=[ben_constants.Country.Austria, ben_constants.Country.Kosovo],
        )
    )
    assert len(
        build_set(
            "S1",
            seasons=[ben_constants.Season.Winter],
            remove_unrecommended_dl_patches=True,
        )
    ) < len(
        build_set(
            "S1",
            seasons=[ben_constants.Season.Winter],
            remove_unrecommended_dl_patches=False,
        )
    )


@pytest.mark.parametrize(
    "inp_kwargs",
    [
        dict(seasons=ben_constants.Season.Winter),
        dict(countries="winter"),
        dict(countries="wintr"),
        dict(countries="Astria"),
        dict(countries="Norway"),
    ],
)
def test_build_set_invalid_input(inp_kwargs):
    with pytest.raises(ValidationError):
        build_set("S1", **inp_kwargs)


def test_build_single_csv_sets(tmp_path: Path):
    fp = tmp_path / "patches"
    build_csv_sets(
        fp,
        ben_constants.SentinelSource.S2,
        seasons=[ben_constants.Season.Summer],
        countries=[ben_constants.Country.Serbia],
        write_separate_splits=False,
    )
    assert fp.with_suffix(".csv").exists()


def test_build_splitted_csv_sets(tmp_path: Path):
    fp = tmp_path / "patches"
    build_csv_sets(
        fp,
        ben_constants.SentinelSource.S1,
        countries=[ben_constants.Country.Kosovo],
        write_separate_splits=True,
    )
    assert fp.with_name(f"{fp.name}_train.csv").exists()
    assert fp.with_name(f"{fp.name}_validation.csv").exists()
    assert fp.with_name(f"{fp.name}_test.csv").exists()
