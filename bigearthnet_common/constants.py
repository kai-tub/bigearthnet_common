# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_constants.ipynb (unless otherwise specified).

__all__ = ['OLD2NEW_LABELS_DICT', 'OLD_LABELS', 'NEW_LABELS', 'OLD_LABELS_TO_IDX', 'NEW_LABELS_TO_IDX',
           'CLC_LV3_TO_LV2', 'CLC_LV2_TO_LV1', 'CLC_LV3_TO_LV1', 'CLC_LV3_LABELS', 'CLC_LV2_LABELS', 'CLC_LV1_LABELS',
           'CLC_LV3_COUNT', 'CLC_LV2_COUNT', 'CLC_LV1_COUNT', 'MAX_VALUES_BY_DTYPE_STR', 'URL', 'BAND_STATS',
           'BAND_STATS_FLOAT32', 'BEN_CHANNELS', 'BEN_10m_CHANNELS', 'BEN_20m_CHANNELS', 'BEN_10m_20m_CHANNELS',
           'BEN_60m_CHANNELS', 'BEN_RGB_CHANNELS', 'BEN_PATCH_SIZE_M', 'BEN_S1_V1_0_JSON_KEYS', 'BEN_S2_V1_0_JSON_KEYS',
           'COUNTRIES', 'COUNTRIES_ISO_A2', 'BEN_COMPLETE_SIZE', 'BEN_SNOWY_PATCHES_COUNT',
           'BEN_CLOUDY_OR_SHADOWY_PATCHES_COUNT', 'BEN_NO_19_CLASS_TARGET_COUNT', 'BEN_RECOMMENDED_SIZE', 'BEN_S2_RE',
           'BEN_S1_RE', 'BEN_S1_BAND_RE', 'BEN_S2_BAND_RE', 'smart_pprint', 'print_all_constants', 'constants_prompt']

# Cell
import fastcore.all as fc
import natsort
import rich
import re


# Cell


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


# Cell
OLD2NEW_LABELS_DICT = {
    "Continuous urban fabric": "Urban fabric",
    "Discontinuous urban fabric": "Urban fabric",
    "Industrial or commercial units": "Industrial or commercial units",
    "Non-irrigated arable land": "Arable land",
    "Permanently irrigated land": "Arable land",
    "Rice fields": "Arable land",
    "Vineyards": "Permanent crops",
    "Fruit trees and berry plantations": "Permanent crops",
    "Olive groves": "Permanent crops",
    "Annual crops associated with permanent crops": "Permanent crops",
    "Pastures": "Pastures",
    "Complex cultivation patterns": "Complex cultivation patterns",
    "Land principally occupied by agriculture, with significant areas of natural vegetation": "Land principally occupied by agriculture, with significant areas of natural vegetation",
    "Agro-forestry areas": "Agro-forestry areas",
    "Broad-leaved forest": "Broad-leaved forest",
    "Coniferous forest": "Coniferous forest",
    "Mixed forest": "Mixed forest",
    "Natural grassland": "Natural grassland and sparsely vegetated areas",
    "Sparsely vegetated areas": "Natural grassland and sparsely vegetated areas",
    "Moors and heathland": "Moors, heathland and sclerophyllous vegetation",
    "Sclerophyllous vegetation": "Moors, heathland and sclerophyllous vegetation",
    "Transitional woodland/shrub": "Transitional woodland, shrub",
    "Beaches, dunes, sands": "Beaches, dunes, sands",
    "Inland marshes": "Inland wetlands",
    "Peatbogs": "Inland wetlands",
    "Salt marshes": "Coastal wetlands",
    "Salines": "Coastal wetlands",
    "Water courses": "Inland waters",
    "Water bodies": "Inland waters",
    "Coastal lagoons": "Marine waters",
    "Estuaries": "Marine waters",
    "Sea and ocean": "Marine waters",
    "Airports": None,
    "Bare rock": None,
    "Dump sites": None,
    "Port areas": None,
    "Road and rail networks and associated land": None,
    "Mineral extraction sites": None,
    "Construction sites": None,
    "Sport and leisure facilities": None,
    "Burnt areas": None,
    "Intertidal flats": None,
    "Green urban areas": None,
}

OLD_LABELS = sorted(tuple({k for k in OLD2NEW_LABELS_DICT.keys()}))
NEW_LABELS = sorted(tuple({v for v in OLD2NEW_LABELS_DICT.values() if v is not None}))
OLD_LABELS_TO_IDX = fc.L(OLD_LABELS).val2idx()
NEW_LABELS_TO_IDX = fc.L(NEW_LABELS).val2idx()


# Cell

# Manually copied the LVL3 labels to be able to test for typos from both sources
# Strings copied from
# https://land.copernicus.eu/user-corner/technical-library/corine-land-cover-nomenclature-guidelines/html/index.html
CLC_LV3_TO_LV2 = {
    "Agro-forestry areas": "Heterogeneous agricultural areas",
    "Airports": "Industrial, comercial and transport units",
    "Annual crops associated with permanent crops": "Heterogeneous agricultural areas",
    "Bare rock": "Open spaces with little or no vegetation",
    "Beaches, dunes, sands": "Open spaces with little or no vegetation",
    "Broad-leaved forest": "Forest",
    "Burnt areas": "Open spaces with little or no vegetation",
    "Coastal lagoons": "Marine waters",
    "Complex cultivation patterns": "Heterogeneous agricultural areas",
    "Coniferous forest": "Forest",
    "Construction sites": "Mine, dump and construction sites",
    "Continuous urban fabric": "Urban fabric",
    "Discontinuous urban fabric": "Urban fabric",
    "Dump sites": "Mine, dump and construction sites",
    "Estuaries": "Marine waters",
    "Fruit trees and berry plantations": "Permanent crops",
    "Green urban areas": "Artificial, non-agricultural vegetated areas",
    "Industrial or commercial units": "Industrial, comercial and transport units",
    "Inland marshes": "Inland wetlands",
    "Intertidal flats": "Coastal wetlands",
    "Land principally occupied by agriculture, with significant areas of natural vegetation": "Heterogeneous agricultural areas",
    "Mineral extraction sites": "Mine, dump and construction sites",
    "Mixed forest": "Forest",
    "Moors and heathland": "Shrub and/or herbaceous vegetation associations",
    "Natural grassland": "Shrub and/or herbaceous vegetation associations",
    "Non-irrigated arable land": "Arable land",
    "Olive groves": "Permanent crops",
    "Pastures": "Pastures",
    "Peatbogs": "Inland wetlands",
    "Permanently irrigated land": "Arable land",
    "Port areas": "Industrial, comercial and transport units",
    "Rice fields": "Arable land",
    "Road and rail networks and associated land": "Industrial, comercial and transport units",
    "Salines": "Coastal wetlands",
    "Salt marshes": "Coastal wetlands",
    "Sclerophyllous vegetation": "Shrub and/or herbaceous vegetation associations",
    "Sea and ocean": "Marine waters",
    "Sparsely vegetated areas": "Open spaces with little or no vegetation",
    "Sport and leisure facilities": "Artificial, non-agricultural vegetated areas",
    "Transitional woodland/shrub": "Shrub and/or herbaceous vegetation associations",
    "Vineyards": "Permanent crops",
    "Water bodies": "Inland waters",
    "Water courses": "Inland waters",
    "Glaciers and perpetual snow": "Open spaces with little or no vegetation",
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

CLC_LV3_LABELS = tuple(CLC_LV3_TO_LV2.keys())
CLC_LV2_LABELS = tuple(CLC_LV2_TO_LV1.keys())
CLC_LV1_LABELS = tuple(set(CLC_LV2_TO_LV1.values()))

# manually added to double-check values
CLC_LV3_COUNT = 44
CLC_LV2_COUNT = 15
CLC_LV1_COUNT = 5


# Cell
# Inspired by
# https://github.com/albumentations-team/albumentations/blob/master/albumentations/augmentations/functional.py#L1259
MAX_VALUES_BY_DTYPE_STR = {
    "uint8": 255,
    "uint16": 65535,
    "uint32": 4294967295,
    "float32": 1.0,
    "float64": 1.0,
}


# Cell
URL = "http://bigearth.net/downloads/BigEarthNet-v1.0.tar.gz"

# Stats from https://git.tu-berlin.de/rsim/bigearthnet-models-tf/-/blob/master/BigEarthNet.py
BAND_STATS = {
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

# FUTURE: Double check original values!
# Custom transformation to float32 values.
# Assumes that the original means and std values are encoded in uint16
BAND_STATS_FLOAT32 = {
    k: {
        band: band_val / MAX_VALUES_BY_DTYPE_STR["uint16"]
        for band, band_val in v.items()
    }
    for k, v in BAND_STATS.items()
}

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

# Cell
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


# Cell
COUNTRIES = (
    "Austria",
    "Belgium",
    "Finland",
    "Ireland",
    "Kosovo",
    "Lithuania",
    "Luxembourg",
    "Portugal",
    "Serbia",
    "Switzerland",
)

# NOTE: ISO_A2 because ISO_A3 does is NOT defined for Kosovo!
COUNTRIES_ISO_A2 = (
    "AT",
    "BE",
    "FI",
    "IE",
    "XK",
    "LT",
    "LU",
    "PT",
    "RS",
    "CH",
)


# Cell

BEN_COMPLETE_SIZE = 590_326
BEN_SNOWY_PATCHES_COUNT = 61_707
BEN_CLOUDY_OR_SHADOWY_PATCHES_COUNT = 9_280
# this is before removing cloudy/snowy patches
BEN_NO_19_CLASS_TARGET_COUNT = 57
BEN_RECOMMENDED_SIZE = 519_284


# Cell

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


# Cell

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


# Cell

# works because of greedy regex
BEN_S1_BAND_RE = re.compile(r".*_(?P<band>V[HV])")
BEN_S2_BAND_RE = re.compile(r".*(?P<band>B\d[0-9A])")

# Cell
from rich.table import Table
from functools import singledispatch
from collections.abc import Mapping, Sequence


def _single_column_table(col_name, rows):
    t = Table(col_name)
    for row in rows:
        t.add_row(row)
    return t


def _simple_dict_table(header, dictionary):
    t = Table(title=header, show_header=False)
    for k, v in dictionary.items():
        t.add_row(k, str(v))
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


# Cell
def print_all_constants():
    """
    A function that shows all of the pre-defined constants of the library.
    """
    ben_constants = {
        k: v for k, v in globals().items() if not k.startswith("_") and k.upper() == k
    }
    for k, v in ben_constants.items():
        smart_pprint(k, v)


# Cell
from rich.prompt import Prompt


class _ManyChoicesPrompt(Prompt):
    def make_prompt(self, default):
        """Make prompt text with many choices
        Args:
            default (DefaultType): Default value.
        Returns:
            Text: Text to display in prompt.
        """
        prompt = self.prompt.copy()
        prompt.end = ""

        if self.show_choices and self.choices:
            _choices = "\n\t".join(self.choices)
            choices = f"\n\t{_choices}\n"
            prompt.append(" ")
            prompt.append(choices, "prompt.choices")

        if (
            default != ...
            and self.show_default
            and isinstance(default, (str, self.response_type))
        ):
            prompt.append(" ")
            _default = self.render_default(default)
            prompt.append(_default)

        prompt.append(self.prompt_suffix)

        return prompt


# Cell
def constants_prompt():
    """
    A smart prompt to quickly display common BigEarthNet constants.
    """
    ben_constants = {
        k: v for k, v in globals().items() if not k.startswith("_") and k.upper() == k
    }
    k = _ManyChoicesPrompt.ask(
        "What constant do you want to see?", choices=ben_constants.keys()
    )
    smart_pprint(k, ben_constants[k])


if __name__ == "__main__" and not fc.IN_IPYTHON:
    constants_prompt()
