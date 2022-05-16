from datetime import date
from importlib import resources
from typing import Counter

import fastcore.test as fc_test
import pytest
from dateutil.parser import ParserError
from pydantic import ValidationError
from rich.table import Table

import bigearthnet_common
from bigearthnet_common.base import *


@pytest.fixture
def s2_json_folder():
    dir_path = Path(__file__).parent / "S2_json_only"
    return dir_path.absolute()


@pytest.fixture
def s1_json_folder():
    dir_path = Path(__file__).parent / "S1_json_only"
    return dir_path.absolute()


@pytest.fixture
def s2_json_path(s2_json_folder):
    fp = (
        Path(s2_json_folder)
        / "S2A_MSIL2A_20170617T113321_4_55/S2A_MSIL2A_20170617T113321_4_55_labels_metadata.json"
    )
    return fp


@pytest.fixture
def s1_json_path(s1_json_folder):
    fp = (
        Path(s1_json_folder)
        / "S1A_IW_GRDH_1SDV_20170613T165043_33UUP_61_39/S1A_IW_GRDH_1SDV_20170613T165043_33UUP_61_39_labels_metadata.json"
    )
    return fp


@pytest.mark.parametrize("resource", [r.value for r in Resource])
def test_available_resources(resource):
    assert resources.is_resource(bigearthnet_common, resource)


def test_parse_valid_datetime():
    d1 = parse_datetime("2017-06-13 10:10:31")
    d2 = parse_datetime("13.06.2017 10:10:31")
    d3 = parse_datetime(
        datetime(year=2017, month=6, day=13, hour=10, minute=10, second=31)
    )
    fc_test.test_eq(d1, d2)
    fc_test.test_eq(d2, d3)


@pytest.mark.parametrize("time", [42, date(year=2017, month=10, day=1)])
def test_parse_invalid_datetime_type(time):
    with pytest.raises(TypeError, match="parse"):
        parse_datetime(time)


def test_parse_invalid_datetime_format():
    time = "large_tile"
    with pytest.raises(ParserError, match="format"):
        parse_datetime(time)


def test_read_S2_json(s2_json_path):
    s2_data = read_S2_json(s2_json_path)
    assert all(k in ben_constants.BEN_S2_V1_0_JSON_KEYS for k in s2_data)
    assert len(s2_data) == len(ben_constants.BEN_S2_V1_0_JSON_KEYS)


def test_read_S2_invalid_json(s1_json_path):
    with pytest.raises(ValueError, match="missing entries"):
        read_S2_json(s1_json_path)


def test_read_S1_json(s1_json_path):
    s1_data = read_S1_json(s1_json_path)
    assert all(k in ben_constants.BEN_S1_V1_0_JSON_KEYS for k in s1_data)
    assert len(s1_data) == len(ben_constants.BEN_S1_V1_0_JSON_KEYS)


def test_read_S1_invalid_json(s2_json_path):
    with pytest.raises(ValueError, match="missing entries"):
        read_S1_json(s2_json_path)


def test_get_s2_patch_directories(s2_json_folder, s1_json_folder):
    assert len(get_s2_patch_directories(s2_json_folder)) == 2
    assert len(get_s2_patch_directories(s1_json_folder)) == 0


def test_get_s1_patch_directories(s1_json_folder, s2_json_folder):
    assert len(get_s1_patch_directories(s1_json_folder)) == 2
    assert len(get_s1_patch_directories(s2_json_folder)) == 0


def test_get_all_s1_patch_names_against_complete_s1_s2_mapping():
    s1_patches = get_all_s1_patch_names()
    s1_to_s2_mapping = get_complete_s1_to_s2_patch_name_mapping()
    assert s1_patches == set(s1_to_s2_mapping.keys())


def test_get_all_s2_patch_names_against_complete_s2_s1_mapping():
    s2_patches = get_all_s2_patch_names()
    s2_to_s1_mapping = get_complete_s2_to_s1_patch_name_mapping()
    assert s2_patches == set(s2_to_s1_mapping.keys())


def test_s1_s2_and_s2_s1_mapping():
    s1_to_s2_mapping = get_complete_s1_to_s2_patch_name_mapping()
    s2_to_s1_mapping = get_complete_s2_to_s1_patch_name_mapping()

    assert all(
        k == v for k, v in zip(s1_to_s2_mapping.keys(), s2_to_s1_mapping.values())
    )
    assert all(
        k == v for k, v in zip(s1_to_s2_mapping.values(), s2_to_s1_mapping.keys())
    )
    assert len(s1_to_s2_mapping) == ben_constants.BEN_COMPLETE_SIZE


def test_ben_regex_against_s1_s2_and_s2_s1_mapping():
    s1_to_s2_mapping = get_complete_s1_to_s2_patch_name_mapping()
    s2_to_s1_mapping = get_complete_s2_to_s1_patch_name_mapping()
    assert all(
        ben_constants.BEN_S1_RE.fullmatch(s1_patch)
        for s1_patch in s1_to_s2_mapping.keys()
    )
    assert all(
        ben_constants.BEN_S2_RE.fullmatch(s2_patch)
        for s2_patch in s1_to_s2_mapping.values()
    )


def test_country_mapping():
    s2_country_mapping = get_patches_to_country_mapping()
    s1_country_mapping = get_patches_to_country_mapping(use_s2_patch_names=False)
    assert len(s1_country_mapping) == len(s2_country_mapping)
    assert all(
        s1_value == s2_value
        for s1_value, s2_value in zip(
            s1_country_mapping.values(), s2_country_mapping.values()
        )
    )

    # validate that countries are only expected countries
    assert set(s2_country_mapping.values()) == set(ben_constants.COUNTRIES)
    # check by visual inspection
    assert s2_country_mapping["S2A_MSIL2A_20171221T112501_56_35"] == "Portugal"


@pytest.mark.parametrize(
    "inp",
    [
        "S2A_MSIL2A_20171221T112501_56_35",
        "S1A_IW_GRDH_1SDV_20171221T064238_29SND_56_35",
    ],
)
def test_get_country(inp):
    assert get_country_from_patch_name(inp) == "Portugal"


def test_season_mapping():
    s2_season_mapping = get_patches_to_season_mapping()
    s1_season_mapping = get_patches_to_season_mapping(use_s2_patch_names=False)
    assert len(s1_season_mapping) == len(s2_season_mapping)
    assert all(
        s1_value == s2_value
        for s1_value, s2_value in zip(
            s1_season_mapping.values(), s2_season_mapping.values()
        )
    )

    # There are only 4 seasons
    assert len(set(s2_season_mapping.values())) == 4
    assert set(s2_season_mapping.values()) == set(s for s in ben_constants.Season)
    # check by inspecting the acquisition time
    assert (
        s2_season_mapping["S2A_MSIL2A_20171221T112501_56_35"]
        == ben_constants.Season.Winter
    )


# examples from above
@pytest.mark.parametrize(
    "inp",
    [
        "S2A_MSIL2A_20171221T112501_56_35",
        "S1A_IW_GRDH_1SDV_20171221T064238_29SND_56_35",
    ],
)
def test_get_season(inp):
    assert get_season_from_patch_name(inp) == ben_constants.Season.Winter


def test_s1_and_s2_snow_patches():
    s2_snow_patches = get_s2_patches_with_seasonal_snow()
    assert len(s2_snow_patches) == ben_constants.BEN_SNOWY_PATCHES_COUNT
    s1_snow_patches = get_s1_patches_with_seasonal_snow()
    assert len(s1_snow_patches) == ben_constants.BEN_SNOWY_PATCHES_COUNT


def test_s1_and_s2_cloud_and_shadow_patches():
    s2_cloud_and_shadow_patches = get_s2_patches_with_cloud_and_shadow()
    assert (
        len(s2_cloud_and_shadow_patches)
        == ben_constants.BEN_CLOUDY_OR_SHADOWY_PATCHES_COUNT
    )
    s1_cloud_and_shadow_patches = get_s1_patches_with_cloud_and_shadow()
    assert (
        len(s1_cloud_and_shadow_patches)
        == ben_constants.BEN_CLOUDY_OR_SHADOWY_PATCHES_COUNT
    )


@pytest.mark.parametrize(
    "inp,exp",
    [
        ("hello", False),
        ("S2A_MSIL2A_20180205T100211_2_0", True),
        ("S1A_IW_GRDH_1SDV_20180417T155012_34WFV_59_20", True),
        ("S2B_MSIL2A_20170906T101019_33_85", False),
        ("S1A_IW_GRDH_1SDV_20170904T161304_34VDN_33_85", False),
    ],
)
def test_is_snowy_patch(inp, exp):
    assert is_snowy_patch(inp) == exp


def test_get_patches_with_no_19_class_targets():
    assert (
        len(get_s2_patches_with_no_19_class_target())
        == ben_constants.BEN_NO_19_CLASS_TARGET_COUNT
    )
    assert (
        len(get_s1_patches_with_no_19_class_target())
        == ben_constants.BEN_NO_19_CLASS_TARGET_COUNT
    )

    # contains a single patch which is snowy
    s2_patches_no_19_class = get_s2_patches_with_no_19_class_target()
    no_snowy = {p for p in s2_patches_no_19_class if not is_snowy_patch(p)}
    assert len(no_snowy) < len(s2_patches_no_19_class)

    # contains a single patch which is cloudy
    s2_patches_no_19_class = get_s2_patches_with_no_19_class_target()
    no_clouds = {p for p in s2_patches_no_19_class if not is_cloudy_shadowy_patch(p)}
    assert len(no_clouds) < len(s2_patches_no_19_class)


@pytest.mark.parametrize(
    "inp,exp",
    [
        ("S2A_MSIL2A_20171221T112501_56_35", True),
        ("S1A_IW_GRDH_1SDV_20171221T064238_29SND_56_35", True),
        ("S1A_IW_GRDH_1SDV_20170716T180622_29UPV_72_73", False),
        ("S2A_MSIL2A_20170717T113321_61_13", False),
    ],
)
def test_has_19_class_target(inp, exp):
    assert has_19_class_target(inp) == exp


def test_original_splits():
    s2_train = get_s2_patches_from_original_train_split()
    s1_train = get_s1_patches_from_original_train_split()

    s2_val = get_s2_patches_from_original_validation_split()
    s1_val = get_s1_patches_from_original_validation_split()

    s2_test = get_s2_patches_from_original_test_split()
    s1_test = get_s1_patches_from_original_test_split()

    assert len(s2_test) < len(s2_train)
    assert len(s2_val) < len(s2_train)
    assert len(s1_train) == len(s2_train)
    assert len(s1_val) == len(s2_val)
    assert len(s1_test) == len(s2_test)


@pytest.mark.parametrize(
    "inp,exp",
    [
        ("S2A_MSIL2A_20170717T113321_28_87", "train"),
        ("S2B_MSIL2A_20170812T092029_75_6", "validation"),
        ("S2A_MSIL2A_20170717T113321_28_88", "test"),
        # s1
        ("S1A_IW_GRDH_1SDV_20170802T163350_34TCR_78_45", "train"),
        ("S1B_IW_GRDH_1SDV_20170701T182622_29SND_64_30", "validation"),
        ("S2A_MSIL2A_20170717T113321_28_88", "test"),
    ],
)
def test_get_original_split_from_patch_name(inp, exp):
    assert get_original_split_from_patch_name(inp) == exp


@pytest.mark.parametrize(
    "inp",
    [
        # snowy patch
        "S2B_MSIL2A_20170906T101019_33_85",
        "S1A_IW_GRDH_1SDV_20170904T161304_34VDN_33_85",
        "wrong_input",
    ],
)
def test_get_original_split_from_invalid_patches(inp):
    # with warnings.catch_warnings(record=True) as w:
    #     warnings.simplefilter("always")
    with pytest.warns(UserWarning):
        assert get_original_split_from_patch_name(inp) is None
        # assert len(w) == 1
        # assert issubclass(w[-1].category, UserWarning)


def test_old2new_labels():
    assert old2new_labels(
        [
            "Continuous urban fabric",
            "Discontinuous urban fabric",
        ]
    ) == ["Urban fabric", "Urban fabric"]


def test_old2new_labels_dropped_inputs():
    with pytest.warns(UserWarning):
        assert old2new_labels(("Burnt areas",)) is None


def test_old2new_labels_invalid_inputs():
    with pytest.raises(KeyError):
        old2new_labels(["Illegal input label"])


@pytest.mark.parametrize(
    "inp",
    [
        ("Agro-forestry areas",),
        ("Agro-forestry areas", "Arable land"),
    ],
)
def test_19_labels_to_multi_hot(inp):
    multi = ben_19_labels_to_multi_hot(inp)
    c = Counter(multi)
    assert c[1.0] == len(inp)
    assert c[0.0] == 19 - len(inp)


def test_19_labels_to_multi_hot_order():
    inp = ("Agro-forestry areas", "Arable land")
    multi = ben_19_labels_to_multi_hot(inp, lex_sorted=True)
    assert multi[0] == 1
    assert multi[1] == 1
    # https://git.tu-berlin.de/rsim/BigEarthNet-S2_19-classes_models/-/raw/master/label_indices.json
    multi = ben_19_labels_to_multi_hot(inp, lex_sorted=False)
    assert multi[0] == 0
    # This fails!
    assert multi[7] == 1
    assert multi[2] == 1


def test_19_labels_to_multi_hot_invalid():
    with pytest.raises(KeyError):
        ben_19_labels_to_multi_hot(["Airport"])


@pytest.mark.parametrize(
    "inp",
    [
        ("Agro-forestry areas",),
        ("Agro-forestry areas", "Airports"),
    ],
)
def test_43_labels_to_multi_hot(inp):
    multi43 = ben_43_labels_to_multi_hot(inp)
    c = Counter(multi43)
    assert c[1.0] == len(inp)
    assert c[0.0] == 43 - len(inp)


def test_43_labels_to_multi_hot_order():
    inp = ("Agro-forestry areas", "Airports")
    multi = ben_43_labels_to_multi_hot(inp, lex_sorted=True)
    assert multi[0] == 1
    assert multi[1] == 1
    # https://git.tu-berlin.de/rsim/BigEarthNet-S2_19-classes_models/-/raw/master/label_indices.json
    multi = ben_43_labels_to_multi_hot(inp, lex_sorted=False)
    assert multi[0] == 0
    assert multi[21] == 1
    assert multi[5] == 1


def test_43_labels_to_multi_hot_invalid():
    with pytest.raises(KeyError):
        ben_43_labels_to_multi_hot(["Arable land"])


def test_multi_hot_numpy_compability():
    import numpy as np

    inp_19 = ["Arable land"]
    assert ben_19_labels_to_multi_hot(np.array(inp_19)) == ben_19_labels_to_multi_hot(
        inp_19
    )

    inp_43 = ["Airports"]
    assert ben_43_labels_to_multi_hot(np.array(inp_43)) == ben_43_labels_to_multi_hot(
        inp_43
    )


def test_validate_ben_s1_root_directory(s1_json_folder):
    # the json path has no bands files and, therefore, contains no valid data
    assert (
        len(validate_ben_s1_root_directory(s1_json_folder))
        == ben_constants.BEN_COMPLETE_SIZE
    )


def test_validate_ben_s2_root_directory(s2_json_folder):
    assert (
        len(validate_ben_s2_root_directory(s2_json_folder))
        == ben_constants.BEN_COMPLETE_SIZE
    )


@pytest.mark.parametrize(
    "inp",
    [
        ["S1A_IW_GRDH_1SDV_20170613T165043_33UUP_87_48"],
        ["S2A_MSIL2A_20170613T101031_87_48"],
        [
            "S1A_IW_GRDH_1SDV_20170613T165043_33UUP_87_48",
            "S2A_MSIL2A_20170613T101031_87_48",
        ],
    ],
)
def test_describe_patch(inp):
    t = describe_patch(inp)
    assert isinstance(t, Table)
    assert t.row_count == len(inp)


def test_describe_patch_invalid_name():
    with pytest.raises(ValueError, match="not a valid S1/S2 patch name!"):
        describe_patch(["invalid-patch-name"])


def test_describe_patch_invalid_type():
    with pytest.raises(ValidationError):
        describe_patch("not-a-list")
