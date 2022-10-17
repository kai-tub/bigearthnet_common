import re
from enum import Enum

import natsort
import rich


def _generate_old2new_labels_dict():
    """
    Code used to generate Old2New_labels dictionary.
    Only run once and saved the output as a constant.
    """
    import requests

    src_url = "https://git.tu-berlin.de/rsim/BigEarthNet-S2_19-classes_models/-/raw/master/label_indices.json"
    r = requests.get(src_url)
    src = r.json()
    original_labels = list(src["original_labels"].keys())
    assert len(original_labels) == 43
    new_labels = list(src["BigEarthNet-19_labels"].keys())
    assert len(new_labels) == 19
    label_conv = src["label_conversion"]
    assert len(label_conv) == len(new_labels)

    # d = {}
    # for new_label_idx, old_label_idxs in enumerate(label_conv):
    #     for old_label_idx in old_label_idxs:
    #         d[original_labels[old_label_idx]] = new_labels[new_label_idx]

    # print(d)

    old2new_label_mapping = {
        original_labels[old_idx]: new_labels[new_label_idx]
        for new_label_idx, row in enumerate(src["label_conversion"])
        for old_idx in row
    }

    deleted_labels = set(original_labels) - set(old2new_label_mapping.keys())

    for l in deleted_labels:
        old2new_label_mapping[l] = None

    assert len(old2new_label_mapping.keys()) == len(original_labels)

    return old2new_label_mapping


# Same order as in the original BigEarthNet code:
# https://git.tu-berlin.de/rsim/BigEarthNet-S2_19-classes_models/-/raw/master/label_indices.json
OLD2NEW_LABELS_DICT = {
    "Continuous urban fabric": "Urban fabric",
    "Discontinuous urban fabric": "Urban fabric",
    "Industrial or commercial units": "Industrial or commercial units",
    "Road and rail networks and associated land": None,
    "Port areas": None,
    "Airports": None,
    "Mineral extraction sites": None,
    "Dump sites": None,
    "Construction sites": None,
    "Green urban areas": None,
    "Sport and leisure facilities": None,
    "Non-irrigated arable land": "Arable land",
    "Permanently irrigated land": "Arable land",
    "Rice fields": "Arable land",
    "Vineyards": "Permanent crops",
    "Fruit trees and berry plantations": "Permanent crops",
    "Olive groves": "Permanent crops",
    "Pastures": "Pastures",
    "Annual crops associated with permanent crops": "Permanent crops",
    "Complex cultivation patterns": "Complex cultivation patterns",
    "Land principally occupied by agriculture, with significant areas of natural vegetation": "Land principally occupied by agriculture, with significant areas of natural vegetation",
    "Agro-forestry areas": "Agro-forestry areas",
    "Broad-leaved forest": "Broad-leaved forest",
    "Coniferous forest": "Coniferous forest",
    "Mixed forest": "Mixed forest",
    "Natural grassland": "Natural grassland and sparsely vegetated areas",
    "Moors and heathland": "Moors, heathland and sclerophyllous vegetation",
    "Sclerophyllous vegetation": "Moors, heathland and sclerophyllous vegetation",
    "Transitional woodland/shrub": "Transitional woodland, shrub",
    "Beaches, dunes, sands": "Beaches, dunes, sands",
    "Bare rock": None,
    "Sparsely vegetated areas": "Natural grassland and sparsely vegetated areas",
    "Burnt areas": None,
    "Inland marshes": "Inland wetlands",
    "Peatbogs": "Inland wetlands",
    "Salt marshes": "Coastal wetlands",
    "Salines": "Coastal wetlands",
    "Intertidal flats": None,
    "Water courses": "Inland waters",
    "Water bodies": "Inland waters",
    "Coastal lagoons": "Marine waters",
    "Estuaries": "Marine waters",
    "Sea and ocean": "Marine waters",
}


# Use sorted order as default => Same encoding as used in torchgeo
# https://torchgeo.readthedocs.io/en/latest/api/datasets.html#bigearthnet
OLD_LABELS_ORIGINAL_ORDER = tuple(k for k in OLD2NEW_LABELS_DICT.keys())
OLD_LABELS = sorted(OLD_LABELS_ORIGINAL_ORDER)

# The following would break the original order
# NEW_LABELS_ORIGINAL_ORDER = tuple(
#     {v for v in OLD2NEW_LABELS_DICT.values() if v is not None}
# )
NEW_LABELS_ORIGINAL_ORDER = (
    "Urban fabric",
    "Industrial or commercial units",
    "Arable land",
    "Permanent crops",
    "Pastures",
    "Complex cultivation patterns",
    "Land principally occupied by agriculture, with significant areas of natural vegetation",
    "Agro-forestry areas",
    "Broad-leaved forest",
    "Coniferous forest",
    "Mixed forest",
    "Natural grassland and sparsely vegetated areas",
    "Moors, heathland and sclerophyllous vegetation",
    "Transitional woodland, shrub",
    "Beaches, dunes, sands",
    "Inland wetlands",
    "Coastal wetlands",
    "Inland waters",
    "Marine waters",
)
NEW_LABELS = sorted(NEW_LABELS_ORIGINAL_ORDER)


# Manually copied the LVL3 labels to be able to test for typos from both sources
# Strings copied from
# https://land.copernicus.eu/user-corner/technical-library/corine-land-cover-nomenclature-guidelines/html/index.html
CLC_LV3_TO_LV2 = {
    "Continuous urban fabric": "Urban fabric",
    "Discontinuous urban fabric": "Urban fabric",
    "Industrial or commercial units": "Industrial, comercial and transport units",
    "Road and rail networks and associated land": "Industrial, comercial and transport units",
    "Port areas": "Industrial, comercial and transport units",
    "Airports": "Industrial, comercial and transport units",
    "Mineral extraction sites": "Mine, dump and construction sites",
    "Dump sites": "Mine, dump and construction sites",
    "Construction sites": "Mine, dump and construction sites",
    "Green urban areas": "Artificial, non-agricultural vegetated areas",
    "Sport and leisure facilities": "Artificial, non-agricultural vegetated areas",
    "Non-irrigated arable land": "Arable land",
    "Permanently irrigated land": "Arable land",
    "Rice fields": "Arable land",
    "Vineyards": "Permanent crops",
    "Fruit trees and berry plantations": "Permanent crops",
    "Olive groves": "Permanent crops",
    "Pastures": "Pastures",
    "Annual crops associated with permanent crops": "Heterogeneous agricultural areas",
    "Complex cultivation patterns": "Heterogeneous agricultural areas",
    "Land principally occupied by agriculture, with significant areas of natural vegetation": "Heterogeneous agricultural areas",
    "Agro-forestry areas": "Heterogeneous agricultural areas",
    "Broad-leaved forest": "Forest",
    "Coniferous forest": "Forest",
    "Mixed forest": "Forest",
    "Natural grassland": "Shrub and/or herbaceous vegetation associations",
    "Moors and heathland": "Shrub and/or herbaceous vegetation associations",
    "Sclerophyllous vegetation": "Shrub and/or herbaceous vegetation associations",
    "Transitional woodland/shrub": "Shrub and/or herbaceous vegetation associations",
    "Beaches, dunes, sands": "Open spaces with little or no vegetation",
    "Bare rock": "Open spaces with little or no vegetation",
    "Sparsely vegetated areas": "Open spaces with little or no vegetation",
    "Burnt areas": "Open spaces with little or no vegetation",
    "Glaciers and perpetual snow": "Open spaces with little or no vegetation",
    "Inland marshes": "Inland wetlands",
    "Peatbogs": "Inland wetlands",
    "Salt marshes": "Coastal wetlands",
    "Salines": "Coastal wetlands",
    "Intertidal flats": "Coastal wetlands",
    "Water courses": "Inland waters",
    "Water bodies": "Inland waters",
    "Coastal lagoons": "Marine waters",
    "Estuaries": "Marine waters",
    "Sea and ocean": "Marine waters",
}

CLC_LV2_TO_LV1 = {
    "Urban fabric": "Artificial Surfaces",
    "Industrial, comercial and transport units": "Artificial Surfaces",
    "Mine, dump and construction sites": "Artificial Surfaces",
    "Artificial, non-agricultural vegetated areas": "Artificial Surfaces",
    "Arable land": "Agricultural areas",
    "Permanent crops": "Agricultural areas",
    "Pastures": "Agricultural areas",
    "Heterogeneous agricultural areas": "Agricultural areas",
    "Forest": "Forest and seminatural areas",
    "Shrub and/or herbaceous vegetation associations": "Forest and seminatural areas",
    "Open spaces with little or no vegetation": "Forest and seminatural areas",
    "Inland wetlands": "Wetlands",
    "Coastal wetlands": "Wetlands",
    "Inland waters": "Water bodies",
    "Marine waters": "Water bodies",
}

CLC_LV3_TO_LV1 = {lv3: CLC_LV2_TO_LV1[lv2] for lv3, lv2 in CLC_LV3_TO_LV2.items()}
CLC_LV1_LABELS = (
    "Artificial Surfaces",
    "Agricultural areas",
    "Forest and seminatural areas",
    "Wetlands",
    "Water bodies",
)

CLC_LV3_LABELS = tuple(CLC_LV3_TO_LV2.keys())
CLC_LV2_LABELS = tuple(CLC_LV2_TO_LV1.keys())


# manually added to double-check values
CLC_LV3_COUNT = 44
CLC_LV2_COUNT = 15
CLC_LV1_COUNT = 5


CLC_LV1_TO_CLC_CODE = {
    "Artificial Surfaces": 1,
    "Agricultural areas": 2,
    "Forest and seminatural areas": 3,
    "Wetlands": 4,
    "Water bodies": 5,
}
CLC_CODE_TO_CLC_LV1 = {v: k for k, v in CLC_LV1_TO_CLC_CODE.items()}

CLC_LV2_TO_CLC_CODE = {
    "Urban fabric": 11,
    "Industrial, comercial and transport units": 12,
    "Mine, dump and construction sites": 13,
    "Artificial, non-agricultural vegetated areas": 14,
    "Arable land": 21,
    "Permanent crops": 22,
    "Pastures": 23,
    "Heterogeneous agricultural areas": 24,
    "Forest": 31,
    "Shrub and/or herbaceous vegetation associations": 32,
    "Open spaces with little or no vegetation": 33,
    "Inland wetlands": 41,
    "Coastal wetlands": 42,
    "Inland waters": 51,
    "Marine waters": 52,
}
CLC_CODE_TO_CLC_LV2 = {v: k for k, v in CLC_LV2_TO_CLC_CODE.items()}

# Requires knowledge that dict keep ordering in supported Python version
# as well as the correct order in the mappings
CLC_LV3_TO_CLC_CODE = {
    lv3_lbl: f"{CLC_LV2_TO_CLC_CODE[lv2_lbl]}{i}"
    for lv2_lbl in CLC_LV3_TO_LV2.values()
    for i, lv3_lbl in enumerate(
        [k for k, v in CLC_LV3_TO_LV2.items() if v == lv2_lbl], 1
    )
}

CLC_CODE_TO_CLC_LV3 = {v: k for k, v in CLC_LV3_TO_CLC_CODE.items()}


# Inspired by
# https://github.com/albumentations-team/albumentations/blob/master/albumentations/augmentations/functional.py#L1259
MAX_VALUES_BY_DTYPE_STR = {
    "uint8": 255,
    "uint16": 65535,
    "uint32": 4294967295,
    "float32": 1.0,
    "float64": 1.0,
}


URL = "http://bigearth.net/downloads/BigEarthNet-v1.0.tar.gz"

# Stats from https://git.tu-berlin.de/rsim/bigearthnet-models-tf/-/blob/master/BigEarthNet.py
BAND_STATS_S2 = {
    "mean": {
        "B01": 340.76769064,
        "B02": 429.9430203,
        "B03": 614.21682446,
        "B04": 590.23569706,
        "B05": 950.68368468,
        "B06": 1792.46290469,
        "B07": 2075.46795189,
        "B08": 2218.94553375,
        "B8A": 2266.46036911,
        "B09": 2246.0605464,
        "B11": 1594.42694882,
        "B12": 1009.32729131,
    },
    "std": {
        "B01": 554.81258967,
        "B02": 572.41639287,
        "B03": 582.87945694,
        "B04": 675.88746967,
        "B05": 729.89827633,
        "B06": 1096.01480586,
        "B07": 1273.45393088,
        "B08": 1365.45589904,
        "B8A": 1356.13789355,
        "B09": 1302.3292881,
        "B11": 1079.19066363,
        "B12": 818.86747235,
    },
}
BAND_STATS_S1 = {
    "mean": {
        "VV": -12.619993741972035,
        "VH": -19.29044597721542,
        "VV/VH": 0.6525036195871579,
    },
    "std": {
        "VV": 5.115911777546365,
        "VH": 5.464428464912864,
        "VV/VH": 30.75264076801808,
    },
}

# I am not sure if this should be used!
# FUTURE: Double check original values!
# Custom transformation to float32 values.
# Assumes that the original means and std values are encoded in uint16
# BAND_STATS_FLOAT32 = {
#     k: {
#         band: band_val / MAX_VALUES_BY_DTYPE_STR["uint16"]
#         for band, band_val in v.items()
#     }
#     for k, v in BAND_STATS.items()
# }

BEN_CHANNELS = (
    "B01",
    "B02",
    "B03",
    "B04",
    "B05",
    "B06",
    "B07",
    "B08",
    "B8A",
    "B09",
    "B11",
    "B12",
)

BEN_10m_CHANNELS = (
    "B02",
    "B03",
    "B04",
    "B08",
)

BEN_20m_CHANNELS = (
    "B05",
    "B06",
    "B07",
    "B8A",
    "B11",
    "B12",
)

BEN_10m_20m_CHANNELS = natsort.natsorted(BEN_10m_CHANNELS + BEN_20m_CHANNELS)

BEN_60m_CHANNELS = (
    "B01",
    "B09",
)

# Correctly ordered
BEN_RGB_CHANNELS = (
    "B04",
    "B03",
    "B02",
)

BEN_PATCH_SIZE_M = 1200


BEN_S1_V1_0_JSON_KEYS = {
    "acquisition_time",
    "coordinates",
    "labels",
    "projection",
    "scene_source",
    "corresponding_s2_patch",
}

# note that there is a small difference between S1/S2
# acquisition_time vs acquisition_date
BEN_S2_V1_0_JSON_KEYS = {
    "acquisition_date",
    "coordinates",
    "labels",
    "projection",
    "tile_source",
}

BEN_S1_V1_0_TAR_MD5SUM = "94ced73440dea8c7b9645ee738c5a172"
BEN_S2_V1_0_TAR_MD5SUM = "5a64e9ce38deb036a435a7b59494924c"


class SentinelSource(str, Enum):
    """
    BigEarthNet Sentinel-Source S1 or S2.
    """

    S1 = "S1"
    S2 = "S2"

    def __str__(self):
        return self.value


class Season(str, Enum):
    """
    Seasons of the year.
    """

    Winter = "Winter"
    Fall = "Fall"
    Summer = "Summer"
    Spring = "Spring"

    def __str__(self):
        return self.value


_COUNTRY_TO_ISO_A2 = {
    "Austria": "AT",
    "Belgium": "BE",
    "Finland": "FI",
    "Ireland": "IE",
    "Kosovo": "XK",
    "Lithuania": "LT",
    "Luxembourg": "LU",
    "Portugal": "PT",
    "Serbia": "RS",
    "Switzerland": "CH",
}


class Country(str, Enum):
    """
    Official BigEarthNet countries
    """

    Austria = "Austria"
    Belgium = "Belgium"
    Finland = "Finland"
    Ireland = "Ireland"
    Kosovo = "Kosovo"
    Lithuania = "Lithuania"
    Luxembourg = "Luxembourg"
    Portugal = "Portugal"
    Serbia = "Serbia"
    Switzerland = "Switzerland"

    def to_iso_A2(self):
        return _COUNTRY_TO_ISO_A2[self.value]

    def __str__(self):
        return self.value


class Split(str, Enum):
    """
    Official split _names_ to keep the naming consistent.
    """

    train = "train"
    validation = "validation"
    test = "test"

    def __str__(self):
        return self.value


COUNTRIES = tuple(c for c in Country)

# NOTE: ISO_A2 because ISO_A3 does is NOT defined for Kosovo!
COUNTRIES_ISO_A2 = tuple(c.to_iso_A2() for c in Country)


BEN_COMPLETE_SIZE = 590_326
BEN_SNOWY_PATCHES_COUNT = 61_707
BEN_CLOUDY_OR_SHADOWY_PATCHES_COUNT = 9_280
# this is before removing cloudy/snowy patches
BEN_NO_19_CLASS_TARGET_COUNT = 57
BEN_RECOMMENDED_SIZE = 519_284


# From: https://depositonce.tu-berlin.de/bitstream/11303/11261/3/BigEarthNetManual.pdf
# Ignoring the mistakenly leading 0 in vertical and horizontal patch.
# Ignore the bug where the hour digits do not necessarily have a leading 0

BEN_S2_RE = re.compile(
    r"""
        (?P<sentinel_mission>S2[AB])
        _
        MSIL2A # Sentinel-2 data product
        _
        (?P<year>\d{4})
        (?P<month>\d{2})
        (?P<day>\d{2})
        T
        (?P<hour>\d{1,2}) # Bug
        (?P<minute>\d{2})
        (?P<second>\d{2})
        _
        (?P<horizontal_id>\d{1,2})
        _
        (?P<vertical_id>\d{1,2})
    """,
    re.VERBOSE,
)


# https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-1-sar/naming-conventions
BEN_S1_RE = re.compile(
    r"""
        (?P<sentinel_mission>S1[AB])
        _
        IW # Interferometric Wide swath
        _
        GRDH # Ground-Range-Detection High Resolution
        _
        1   # processing level 1
        S   # Product class Standard
        DV  # Polarisation dual VV+VH polarisation
        _
        (?P<year>\d{4})
        (?P<month>\d{2})
        (?P<day>\d{2})
        T
        # Inspired by the bug from Sentinel-2
        # Checked all _current_ Sentinel-1 patches
        # and all of them use two digits for hour
        (?P<hour>\d{1,2})
        (?P<minute>\d{2})
        (?P<second>\d{2})
        _
        (?P<sentinel_2_l1c_tile_area>\w{5})
        _
        (?P<horizontal_id>\d{1,2})
        _
        (?P<vertical_id>\d{1,2})
    """,
    re.VERBOSE,
)


# works because of greedy regex
BEN_S1_BAND_RE = re.compile(r".*_(?P<band>V[HV])")
BEN_S2_BAND_RE = re.compile(r".*(?P<band>B\d[0-9A])")


# patch that lies outside of Finland and is easily missed
# by simply intersection calculations based on country shapefiles
# as it would probably belong to Russia
PATCH_FROM_RUSSIA = "S2B_MSIL2A_20180221T093029_65_1"
# patch that lies in the sea-region of Finland
PATCH_IN_TERROTORIAL_WATERS = "S2B_MSIL2A_20170814T100029_33_77"

from collections.abc import Mapping, Sequence
from functools import reduce, singledispatch

from rich.table import Table


def _single_column_table(col_name, rows):
    t = Table(col_name)
    for row in rows:
        t.add_row(row)
    return t


def _simple_dict_table(header, dictionary):
    t = Table(title=header, show_header=False)
    for k, v in dictionary.items():
        t.add_row(str(k), str(v))
    return t


def _default_pprint(value, name):
    rich.print(f"{name}: ", value)


@singledispatch
def _smart_pprint(value, name):
    _default_pprint(value, name)


@_smart_pprint.register
def _(value: Mapping, name):
    if all(isinstance(v, (str, int, float)) or v is None for v in value.values()):
        t = _simple_dict_table(name, value)
        rich.print(t)
    else:
        _default_pprint(value, name)


@_smart_pprint.register
def _(value: str, name):
    # default_pprint str and not call Sequence branch
    _default_pprint(value, name)


@_smart_pprint.register
def _(value: Sequence, name):
    if all(isinstance(entry, str) for entry in value):
        t = _single_column_table(name, value)
        rich.print(t)
    else:
        _default_pprint(value, name)


def smart_pprint(name, value):
    """
    A small `rich.print` wrapper that tries to guess a good representation
    for variable named `name` with the given `value`.
    If no match is found, the function will simply call `rich.print` under the hood.
    Lists of basic types will be printed as a single column list, whereas simple
    dictionaries will be printed as two-column tables, for example.
    """
    _smart_pprint(value, name)


def print_all_constants():
    """
    A function that shows all of the pre-defined constants of the library.
    """
    ben_constants = {
        k: v for k, v in globals().items() if not k.startswith("_") and k.upper() == k
    }
    for k, v in ben_constants.items():
        smart_pprint(k, v)


import click

# FUTURE: should use typer with option
# as it provides an easy interface to generate autocompletions for options
# with some more advanced features.


def cli():
    """
    A function that returns a `click` based CLI application.
    Should be called from `__main__`.
    """
    # where name is selected by user via an option
    # and the value is retrieved from the dictionary

    ben_constants = {
        k: v for k, v in globals().items() if not k.startswith("_") and k.upper() == k
    }

    def smart_pprint_constant(**kwargs):
        """
        Quickly visualize BigEarthNet constants.
        Select one or more constants to print.
        """
        # value True if flag set; False otherwise
        for name, set in kwargs.items():
            name = name.upper()  # undo the click normalization "lower"
            name = name.replace("-", "_")  # undo the personal replacement
            if set:
                smart_pprint(name.upper(), ben_constants[name])

    print_func = smart_pprint_constant
    for k in ben_constants.keys():
        print_func = click.option(f"--{k.replace('_', '-')}", is_flag=True)(print_func)

    cmd = click.command()(print_func)
    return cmd()


if __name__ == "__main__":
    # constants_prompt()
    cli()
