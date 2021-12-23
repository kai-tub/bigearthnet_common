# Common BigEarthNet Tools
> A personal collection of common BigEarthNet functions


This library provides a collection of high-level tools to better work with the [BigEarthNet](bigearth.net) dataset.

`ben_common` tries to accomplish three goals:

1. Collect most relevant _constants_ into a single place to reduce the time spent looking for these, like:
   - The 19 or 43 class nomenclature strings
   - URL
   - Band statistics (mean/variance) as integer and float
   - Channel names
   - etc.
2. Provide parsing functions to convert the metadata json files to a [geopandas](https://geopandas.org/en/stable/) [GeoDataFrame's](https://geopandas.org/en/stable/getting_started/introduction.html).
   - Allow for easy top-level statistical analysis of the data in a familiar _pandas_-style 
   - Provide functions to enrich GeoDataFrames with often required BigEarthNet metadata (like the season or country of the patch)
3. Simplify the building procedure by providing a command line interface with reproducible results



## Deep Learning 

One of the main purposes of the dataset is to allow deep learning researchers and practictioners to easily train their model on multi-spectral satellite data.
In that regard, there is a general recommendation to drop patches that are covered by seasonal snow or clouds.
Also, the novel 19-class nomenclature should be preferred over the original 43-class nomenclature.
As a result of these recommendations, some patches have to be _excluded_ from the original raw BigEarthNet dataset that is provided at [BigEarthNet](bigearth.net).
This is especially important for higher-level statistical analysis.

To simplify the procedure of pre-converting the json metadata files, the library provides a single command that will generate a recommended GeoDataFrame with extra metadata (country/season data of each patch), while dropping all patches that are not recommended for deep learning research.

To generate such a GeoDataFrame and store it as an `parquet` file, use:

`python -m bigearthnet_common.gdf_builder build-recommended-parquet`

If you want to simply read the raw json files and convert those to a GeoDataFrame file, without dropping any patches or adding any metadata, use:

`python -m bigearthnet_common.gdf_builder build-raw-ben-parquet`


## Local Installation

Use [just](https://github.com/casey/just#installation) to install the package or run steps from `justfile` directly.
Requires [mamba](https://github.com/mamba-org/mamba) (highly recommended) or [poetry](https://python-poetry.org/docs/basic-usage/) to be installed.

## Local Documentation
{% include note.html content='Building and serving the documentation requires `Docker` to be installed!' %}
After creating the `ben_common_env` environment, simply run 
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

To review the source code, please take a look at the corresponding `ipynb` notebook from the `nbs` folder.
These notebooks include extensive documentation, visualizations, and tests.
The automatically generated Python files are available in the `bigearthnet_common` module.

