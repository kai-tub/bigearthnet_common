# Common BigEarthNet Tools
> A personal collection of common tools to interact with the BigEarthNet dataset.


<div align="center">

[![Tests](https://img.shields.io/github/workflow/status/kai-tub/bigearthnet_common/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/bigearthnet_common/actions/workflows/main.yml)
[![License](https://img.shields.io/pypi/l/bigearthnet_common?color=dark-green)](https://github.com/kai-tub/bigearthnet_common/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/bigearthnet-common.svg)](https://pypi.org/project/bigearthnet-common/)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)
</div>

This library provides a collection of high-level tools to better work with the [BigEarthNet](bigearth.net) dataset.

`ben_common` tries to accomplish three goals:

1. Collect the most relevant _constants_ into a single place to reduce the time spent looking for these, like:
   - The 19 or 43 class nomenclature strings
   - URL
   - Band statistics (mean/variance) as integer and float
   - Channel names
   - etc.
2. Provide parsing functions to convert the metadata json files to a [geopandas](https://geopandas.org/en/stable/) [GeoDataFrame's](https://geopandas.org/en/stable/getting_started/introduction.html).
   - Allow for easy top-level statistical analysis of the data in a familiar _pandas_-style 
   - Provide functions to enrich GeoDataFrames with often required BigEarthNet metadata (like the season or country of the patch)
3. Simplify the building procedure by providing a command-line interface with reproducible results



## Deep Learning 

One of the main purposes of the dataset is to allow deep learning researchers and practitioners to train their model on multi-spectral satellite data easily.
In that regard, there is a general recommendation to drop patches that are covered by seasonal snow or clouds.
Also, the novel 19-class nomenclature should be preferred over the original 43-class nomenclature.
As a result of these recommendations, some patches have to be _excluded_ from the original raw BigEarthNet dataset that is provided at [BigEarthNet](bigearth.net).
This is especially important for higher-level statistical analysis.

To simplify the procedure of pre-converting the json metadata files, the library provides a single command that will generate a recommended GeoDataFrame with extra metadata (country/season data of each patch) while dropping all patches that are not recommended for deep learning research.

To generate such a GeoDataFrame and store it as an `parquet` file, use:

- `ben_gdf_builder build-recommended-parquet` (available after installing package) or
- `python -m bigearthnet_common.gdf_builder build-recommended-parquet`

If you want to read the raw json files and convert those to a GeoDataFrame file, without dropping any patches or adding any metadata, use:

- `ben_gdf_builder build-raw-ben-parquet` (available after installing package) or
- `python -m bigearthnet_common.gdf_builder build-raw-ben-parquet`


## Local Installation

Use [just](https://github.com/casey/just#installation) to install the package or run steps from `justfile` directly.
Requires [mamba](https://github.com/mamba-org/mamba) (highly recommended) or [poetry](https://python-poetry.org/docs/basic-usage/) to be installed.

## Local Documentation
{% include note.html content='Building and serving the documentation requires `Docker` to be installed!' %}
After creating the `ben_common_env` environment, run 
```bash
docker-compose up
```

Or with `just`:
```bash
just docs
```

After running the command, the documentation server will be available at 
- <http://0.0.0.0:4000/bigearthnet_common/> or 
- <http://localhost:4000/bigearthnet_common/> (WSL).

To review the source code, please look at the corresponding `ipynb` notebook from the `nbs` folder.
These notebooks include extensive documentation, visualizations, and tests.
The automatically generated Python files are available in the `bigearthnet_common` module.

