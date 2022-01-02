# Common BigEarthNet Tools
> A personal collection of common tools to interact with the BigEarthNet dataset.


[![Tests](https://img.shields.io/github/workflow/status/kai-tub/bigearthnet_common/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/bigearthnet_common/actions/workflows/main.yml)
[![License](https://img.shields.io/pypi/l/bigearthnet_common?color=dark-green)](https://github.com/kai-tub/bigearthnet_common/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/bigearthnet-common.svg)](https://pypi.org/project/bigearthnet-common/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/bigearthnet-common?color=dark-green)](https://anaconda.org/conda-forge/bigearthnet-common)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

This library provides a collection of high-level tools to better work with the [BigEarthNet](bigearth.net) dataset.

`ben_common` tries to accomplish three goals:

1. Collect the most relevant _constants_ into a single place to reduce the time spent looking for these, like:
   - The 19 or 43 class nomenclature strings
   - URL
   - Band statistics (mean/variance) as integer and float
   - Channel names
   - etc.
2. Provide parsing functions to convert the metadata JSON files to a [geopandas](https://geopandas.org/en/stable/) [GeoDataFrame](https://geopandas.org/en/stable/getting_started/introduction.html).
   - Allow for easy top-level statistical analysis of the data in a familiar _pandas_-style
   - Provide functions to enrich GeoDataFrames with often required BigEarthNet metadata (like the season or country of the patch)
3. Simplify the building procedure by providing a command-line interface with reproducible results

## Installation
I strongly recommend to use [mamba](https://github.com/mamba-org/mamba) or `conda` with [miniforge](https://github.com/conda-forge/miniforge) to install the package with:
- `mamba/conda install bigearthnet-common -c conda-forge`

As the `bigearthnet_common` tool is built on top of `geopandas` the same restrictions apply.
For more details please review the [geopandas installation documentation](https://geopandas.org/en/stable/getting_started/install.html).

The package is also available via PyPI and could be installed with:
- `pip install bigearthnet_common` (not recommended)

## TL;DR
The most relevant functions are exposed as CLI entry points.
To quickly search for BigEarthNet constants of interest, call:
- `ben_constants_prompt` or
- `python -m bigearthnet_common.constants`

To build the tabular data, use:
- `ben_gdf_builder --help` or
- `python -m bigearthnet_common.ben_gdf_builder --help`


## Deep Learning

One of the primary purposes of the dataset is to allow deep learning researchers and practitioners to train their models on multi-spectral satellite data.
In that regard, there is a general recommendation to drop patches that are covered by seasonal snow or clouds.
Also, the novel 19-class nomenclature should be preferred over the original 43-class nomenclature.
As a result of these recommendations, some patches have to be _excluded_ from the original raw BigEarthNet dataset that is provided at [BigEarthNet](bigearth.net).

To simplify the procedure of pre-converting the JSON metadata files, the library provides a single command that will generate a recommended GeoDataFrame with extra metadata (country/season data of each patch) while dropping all patches that are not recommended for deep learning research.

To generate such a GeoDataFrame and store it as an `parquet` file, use:

- `ben_gdf_builder build-recommended-parquet` (available after installing package) or
- `python -m bigearthnet_common.gdf_builder build-recommended-parquet`

If you want to read the raw JSON files and convert those to a GeoDataFrame file without dropping any patches or adding any metadata, use:

- `ben_gdf_builder build-raw-ben-parquet` (available after installing package) or
- `python -m bigearthnet_common.gdf_builder build-raw-ben-parquet`

## Contributing

Contributions are always welcome!

Please look at the corresponding `ipynb` notebook from the `nbs` folder to review the source code.
These notebooks include extensive documentation, visualizations, and tests.
The automatically generated Python files are available in the `bigearthnet_common` module.

More information is available in the [contributing guidelines](https://github.com/kai-tub/bigearthnet_common/blob/main/.github/CONTRIBUTING.md) document.
