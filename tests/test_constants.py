import pytest

from bigearthnet_common.constants import *


def test_label_sizes():
    assert len(NEW_LABELS) == 19
    assert len(OLD_LABELS) == 43


def test_clc_labels():
    assert len(CLC_LV1_LABELS) == CLC_LV1_COUNT
    assert len(CLC_LV2_LABELS) == CLC_LV2_COUNT
    assert len(CLC_LV3_LABELS) == CLC_LV3_COUNT
    assert set(CLC_LV1_LABELS) == set(CLC_LV3_TO_LV1.values())
    # double checking code [argueably bad-practice]
    assert len(CLC_LV3_TO_LV2.keys()) == CLC_LV3_COUNT
    assert len(CLC_LV2_TO_LV1.keys()) == CLC_LV2_COUNT
    assert len(set(CLC_LV2_TO_LV1.values())) == CLC_LV1_COUNT
    assert (
        len(set(CLC_LV3_TO_LV2.values()) | set(CLC_LV2_TO_LV1.keys())) == CLC_LV2_COUNT
    )


def test_clc_vs_ben_old_labels():
    diff = set(CLC_LV3_LABELS) - set(OLD_LABELS)
    assert len(diff) == 1
    # there was no Glaciers and perpetual snow entry in the BEN dataset!
    assert list(diff)[0] == "Glaciers and perpetual snow"


def test_lv3_code_ordering():
    lv3_codes = list(CLC_LV3_TO_CLC_CODE.values())
    assert all(v1 < v2 for v1, v2 in zip(lv3_codes, lv3_codes[1:]))


def test_ben_channels():
    assert set(BEN_CHANNELS) == set(
        BEN_10m_CHANNELS + BEN_20m_CHANNELS + BEN_60m_CHANNELS
    )
    assert (
        len(set(BEN_10m_CHANNELS) & set(BEN_20m_CHANNELS) & set(BEN_60m_CHANNELS)) == 0
    )


def test_countries_a2():
    assert len(COUNTRIES) == len(COUNTRIES_ISO_A2) == 10


def test_ben_sizes():
    # There is one cloudy patch without a 19-class target:
    # S2A_MSIL2A_20171208T093351_1_64
    # And one snowy patch without a 19-class target:
    # S2B_MSIL2A_20180417T102019_30_1

    # there are no patches that are cloudy and snowy!

    assert BEN_COMPLETE_SIZE == (
        BEN_RECOMMENDED_SIZE
        + BEN_SNOWY_PATCHES_COUNT
        + BEN_CLOUDY_OR_SHADOWY_PATCHES_COUNT
        + BEN_NO_19_CLASS_TARGET_COUNT
        - 2
    )


@pytest.mark.parametrize(
    "inp",
    ["S2A_MSIL2A_20170617T113321_4_55", "S2B_MSIL2A_20170924T93020_41_73"],
)
def test_ben_s2_re_match(inp):
    assert BEN_S2_RE.fullmatch(inp) is not None


@pytest.mark.parametrize(
    "inp",
    ["S2C_MSIL2A_20170617T113321_4_55", "S2A_MSIL2A_20170617T113321_55"],
)
def test_ben_s2_re_no_match(inp):
    assert BEN_S2_RE.fullmatch(inp) is None


@pytest.mark.parametrize(
    "inp",
    [
        "S1A_IW_GRDH_1SDV_20170613T165043_33UUP_61_39",
        "S1A_IW_GRDH_1SDV_20170613T165043_33UUP_61_3",
        # not real patch
        "S1A_IW_GRDH_1SDV_20170613T165043_33UVP_61_39",
    ],
)
def test_ben_s1_re_match(inp):
    assert BEN_S1_RE.fullmatch(inp) is not None


@pytest.mark.parametrize(
    "inp",
    [
        "S1A_IW_GRDH_1SDV_20170613T165043_33UUP_61",
        "S2A_IW_GRDH_1SDV_20170613T165043_33UUP_61",
    ],
)
def test_ben_s1_re_no_match(inp):
    assert BEN_S1_RE.fullmatch(inp) is None


def test_new_label_order():
    assert NEW_LABELS != NEW_LABELS_ORIGINAL_ORDER
    assert NEW_LABELS == sorted(NEW_LABELS_ORIGINAL_ORDER)


def test_old_label_order():
    assert OLD_LABELS != OLD_LABELS_ORIGINAL_ORDER
    assert OLD_LABELS == sorted(OLD_LABELS_ORIGINAL_ORDER)


def test_print_all():
    print_all_constants()
