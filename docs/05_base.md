# BigEarthNet Base Functions

The library provides frequently used functions when working with BigEarthNet.

## Metadata parsing utility functions
The package provides a couple of safe parsing functions that guarantee flexible reading of the default BigEarthNet JSON metadata files.

Usually, you should not use any of these parsing functions directly but use one of the higher-level functions provided by a wrapper library, such as
[bigearthnet_gdf_builder](https://github.com/kai-tub/bigearthnet_gdf_builder).

The relevant functions for parsing are:
- {func}`.read_S1_json`
- {func}`.read_S2_json`

## Patch names utility
To efficiently work with the S1 and S2 patch names simultaneously, the following functions can be used to quickly retrieve a list of all patch names and find the corresponding S1/S2 patch given a reference S2/S1 patch.

- {func}`.s1_to_s2_patch_name`
- {func}`.s2_to_s1_patch_name`

If you want to query the properties of a BigEarthNet patch quickly, you can use the following functions (each allows S1 or S2 patch names as input)

- {func}`.get_original_split_from_patch_name`
- {func}`.is_snowy_patch`
- {func}`.is_cloudy_shadowy_patch`

Or to get a mapping for all patches for the country/season you can access:
- {func}`.get_patches_to_country_mapping`
- {func}`.get_patches_to_season_mapping`

## Label utility functions
A common first step is to convert the old 43-labels to the new [recommended 19-labels](https://arxiv.org/abs/2105.07921) nomenclature.
The package also provides a deterministic way to convert the old/new label nomenclature to a multi-hot encoded list:

- {func}`.old2new_labels`
- {func}`.ben_19_labels_to_multi_hot`
- {func}`.ben_43_labels_to_multi_hot`

:::{important}

Please be aware that there are multiple ways to multi-hot encode the labels.
The functions provide two sensible multi-hot encoding strategies:

- By default, the labels are lexicographically sorted and the index of the sorted list is used as the encoding
    - This is the order of the `NEW_LABELS/OLD_LABELS` constants
    - This ordering is used in the [torchgeo](https://torchgeo.readthedocs.io/en/latest/api/datasets.html#bigearthnet) library
- With `lex_sorted=False` the original ordering is used as the encoding
    - The ordering was defined in the original publication of BigEarthNet in the [labels_indices.json](https://git.tu-berlin.de/rsim/BigEarthNet-S2_19-classes_models/-/raw/master/label_indices.json) file
    - This is the order of the `NEW_LABELS_ORIGINAL_ORDER/OLD_LABELS_ORIGINAL_ORDER` constants

:::

## Describe patch
The library provides a tool to quickly visualize meta-data information about each patch:
- S1 name
- S2 name
- Original Split
- Country
- Season
- Cloudy/Shadowy
- If it has a valid 19-label target

```sh
ben_describe_patch <S1/S2 patch name(s)>
```


## Validating BigEarthNet
One common issue is that due to the size of BigEarthNet, it is not uncommon that the extraction silently fails and that the data is incomplete.
Or that files are accidentally deleted, or worse, only their contents.
The following CLI tools can be used to validate the integrity of the BigEarthNet archive:

```sh
ben_validate_s1_root_dir --help
ben_validate_s2_root_dir --help
```

:::{warning}
Although the implementation works, the function is slow due to many files to check, especially on hard-drive-based servers.
Also, the function will only check if the files exist and are not empty.
They *will not* be validated!
:::
