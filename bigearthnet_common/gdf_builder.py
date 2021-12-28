# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01c_gdf_builder.ipynb (unless otherwise specified).

__all__ = ['COUNTRIES_URL', 'ben_patch_to_gdf', 'ben_patch_to_reprojected_gdf', 'build_gdf_from_patch_paths',
           'get_patch_directories', 'get_gdf_from_patch_dir', 'get_ben_countries_gdf', 'assign_to_ben_country',
           'Season', 'tfm_month_to_season', 'filter_season', 'add_full_ben_metadata', 'remove_bad_ben_gdf_entries',
           'build_raw_ben_parquet', 'extend_ben_parquet', 'remove_discouraged_parquet_entries',
           'build_recommended_parquet']

# Cell
import enum
import json
from pathlib import Path
from typing import List, Union

import fastcore.all as fc
import geopandas
import pandas as pd
import rich.traceback
import typer
from pydantic import DirectoryPath, FilePath, PositiveInt, conint, validate_arguments
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from .base import (
    _download_and_cache_url,
    box_from_ul_lr_coords,
    parse_datetime,
)
from .constants import COUNTRIES, COUNTRIES_ISO_A2

rich.traceback.install(show_locals=True)

COUNTRIES_URL = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip"


# Cell
@validate_arguments
def ben_patch_to_gdf(
    patch_path: Union[FilePath, DirectoryPath]
) -> geopandas.GeoDataFrame:
    """
    Given the filepath to a BigEarthNet json `_metadata_labels` file, or
    to the containing patch folder, the function will return a single row GeoDataFrame.

    The filepath is necessary, as only the filename contains the patch name.

    The datetime will be parsed with best effort and guaranteed to be in the format
    'YYYY-MM-DD hh-mm-ss'

    The coordinates that indicate the upper-left-x/y and lower-right-x/y will be converted
    into a `shapely.Polygon`.

    The coordinate reference system (CRS) will be equivalent to the one given in the json file.
    Or with other words, the data is not reprojected!
    """
    json_path = (
        patch_path
        if patch_path.is_file()
        else patch_path / f"{patch_path.name}_labels_metadata.json"
    )
    try:
        complete_data = json.loads(json_path.read_text())
    except json.JSONDecodeError:
        raise ValueError(f"Error trying to read json from: ", json_path)

    original_json_elements = {"acquisition_date", "coordinates", "labels", "projection", "tile_source"}
    missing_elements = original_json_elements - complete_data.keys()
    if len(missing_elements) > 0:
        raise ValueError(f"{json_path} is missing entries!", missing_elements)

    # ensure that the original values are loaded, as some users may customize the original json files
    data = {k: v for k, v in complete_data.items() if k in original_json_elements}
    data["name"] = json_path.stem.rstrip("_labels_metadata")
    data["acquisition_date"] = parse_datetime(data["acquisition_date"]).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    data["geometry"] = box_from_ul_lr_coords(**data.pop("coordinates"))
    data["labels"] = [data["labels"]]
    crs = data.pop("projection")

    return geopandas.GeoDataFrame(data, crs=crs)


def ben_patch_to_reprojected_gdf(
    patch_path: Union[FilePath, DirectoryPath], target_proj: str = "epsg:4326"
) -> geopandas.GeoDataFrame:
    """
    Calls `ben_patch_to_gdf` and simply reprojects the resulting GeoDataFrame afterwards to the
    given `target_proj`.

    This is a tiny wrapper to ensure that the generated BEN GeoDataFrame's can be concatenated and have a
    common coordinate reference system.

    See `ben_patch_to_gdf` for more details.
    """
    return ben_patch_to_gdf(patch_path).to_crs(target_proj)


# Cell
@validate_arguments
def build_gdf_from_patch_paths(
    patch_paths: List[Path],
    n_workers: PositiveInt = 8,
    progress: bool = True,
    target_proj: str = "epsg:4326",
) -> geopandas.GeoDataFrame:
    """
    Build a single `geopandas.GeoDataFrame` from the BEN json files.
    The code will run in parallel and use `n_workers` processes.
    By default a progress-bar will be shown.

    From personal experience, the ideal number of workers is 8 in most cases.
    For laptops with fewer cores, 2 or 4 `n_workers` should be set.
    More than 8 usually leads to only minor improvements and with n_workers > 12
    the performance usually degrades.

    The function returns a single GDF with all patches reprojected to `target_proj`,
    which is `epsg:4326` by default.
    """
    gdfs = fc.parallel(
        ben_patch_to_reprojected_gdf,
        patch_paths,
        progress=progress,
        n_workers=n_workers,
        target_proj=target_proj,
    )
    if len(gdfs) == 0:
        return geopandas.GeoDataFrame()
    gdf = pd.concat(gdfs, axis=0, ignore_index=True)
    return gdf


# Cell
import re

_ROUGH_BEN_S2_RE = re.compile(r"S\d\w_[^_]+_\d+T\d+_\d+_\d+")


# Cell
@validate_arguments
def get_patch_directories(dir_path: DirectoryPath) -> List[Path]:
    """
    Tries to find all patch directories in the provided `dir_path`.
    The function will use a semi-relaxed regex matching procedure.

    Warning:
    It is currently only verified for BEN-S2 patches.
    """
    return [p for p in dir_path.iterdir() if _ROUGH_BEN_S2_RE.match(p.name) is not None]


@fc.delegates(build_gdf_from_patch_paths)
def get_gdf_from_patch_dir(dir_path: DirectoryPath, **kwargs) -> geopandas.GeoDataFrame:
    """
    Searches through `dir_path` to assemble a BEN-style `GeoDataFrame`.
    Wraps around `get_patch_directory` and `build_gdf_from_patch_paths`.

    Raises an error if an empty GeoDataFrame would be produced.
    """
    patch_paths = get_patch_directories(dir_path)
    gdf = build_gdf_from_patch_paths(patch_paths, **kwargs)
    if len(gdf) == 0:
        raise ValueError("Empty gdf produced! Check provided directory!")
    return gdf


# Cell
def _get_country_borders(force_download: bool = False) -> geopandas.GeoDataFrame:
    "Get all country borders"
    # directly filter out irrelevant lines
    rel_cols = [
        "ISO_A3",
        "ISO_A2",
        "NAME",
        "geometry",
    ]

    file_path = _download_and_cache_url(COUNTRIES_URL, force_download=force_download)

    gdf = geopandas.read_file(file_path)
    return gdf[rel_cols]


# Cell
def get_ben_countries_gdf() -> geopandas.GeoDataFrame:
    """
    Return a `GeoDataFrame` that includes the shapes of each
    country from the BigEarthNet dataset.

    This is a subset of the naturalearthdata 10m-admin-0-countries dataset:

    https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-admin-0-countries
    """
    borders = _get_country_borders()
    ben_borders = borders[borders["ISO_A2"].isin(COUNTRIES_ISO_A2)].copy()
    return ben_borders


# Cell
def assign_to_ben_country(
    gdf: geopandas.GeoDataFrame, crs: str = "epsg:3035"
) -> geopandas.GeoDataFrame:
    """
    Takes a GeoDataFrame as an input and appends a `country` column.
    The `country` column indicates the closest BEN country.

    The function calculates the centroid of each input geometry with the `crs` projection.
    These centroids are then used to find and assign the entry to the closest BEN country.
    Centroids help to more deterministically assign a border-crossing patch to a country.
    For the small BEN patches (1200mx1200m) the _error_ of the approximation is negligible
    and a good heuristic to assign the patch to the country with the largest overlap.
    """
    with Progress(
        TextColumn("{task.description}"),
        SpinnerColumn("bouncingBall"),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task = progress.add_task("Reprojecting", total=1)
        local_gdf = gdf.to_crs(crs)
        progress.update(task, completed=1)

        # has column called NAME for country name
        task = progress.add_task("Loading country shapes", total=1)
        borders = get_ben_countries_gdf()
        borders = borders.to_crs(crs)
        progress.update(task, completed=1)

        task = progress.add_task("Calculating centroids", total=1)
        local_gdf.geometry = local_gdf.geometry.centroid
        progress.update(task, completed=1)

        task = progress.add_task("Assigning data to countries", total=1)
        nn_gdf = local_gdf.sjoin_nearest(borders, how="inner")
        progress.update(task, completed=1)

        gdf["country"] = nn_gdf["NAME"]
    return gdf


# Cell
class Season(str, enum.Enum):
    """
    A simple season class.
    """

    Winter = "Winter"
    Spring = "Spring"
    Summer = "Summer"
    Fall = "Fall"

    @classmethod
    def from_idx(cls, idx):
        return list(cls)[idx]

    def __str__(self):
        return self.value


@validate_arguments
def _month_to_season(month: conint(ge=1, le=12)) -> Season:
    return Season.from_idx(month % 12 // 3)


def tfm_month_to_season(dates: pd.Series) -> pd.Series:
    """
    Uses simple mathmatical formula to transform date
    to seasons string given their months.

    The season is calculated as the meterological season, assuming
    that we are on the northern hemisphere.
    """
    return pd.to_datetime(dates).dt.month.apply(_month_to_season)


# Cell
@validate_arguments
def filter_season(df, date_col: str, season: Season) -> pd.DataFrame:
    seasons = tfm_month_to_season(df[date_col])
    return df[seasons == season]


# Cell
from .base import (
    is_snowy_patch,
    is_cloudy_shadowy_patch,
    old2new_labels,
    get_original_split_from_patch_name,
)


def add_full_ben_metadata(gdf: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
    """
    This is a wrapper around many functions from this library.
    It requires an input `GeoDataFrame` in _BigEarthNet_ style.

    See `get_gdf_from_patch_dir` for details to create a new `GeoDataFrame`.
    This function adds the following columns:

    - `snow`: `bool` - Whether or not the patch contains seasonal snow
    - `cloud_or_shadow`: `bool` - Whether or not the patch contains clouds/shadows
    - `original_split`: One of: `train|validation|test|None`; Indicates to which
        split the patch was originally assigned to
    - `new_labels`: `label|None` - The 19-label nomenclature or None if
        no target labels exist.
    - `country`: `str` - The name of the BigEarthNet country the patch belongs to.
    - `season`: `str` - The season in which the tile was aquired.

    In short, the function will add all the available metadata.
    """
    required_col_names = {"acquisition_date", "name", "labels"}
    diff = required_col_names - set(gdf.columns)
    if len(diff) != 0:
        raise ValueError("The provided gdf is missing columns: ", diff)

    gdf["snow"] = gdf["name"].apply(is_snowy_patch)
    gdf["cloud_or_shadow"] = gdf["name"].apply(is_cloudy_shadowy_patch)
    gdf["new_labels"] = gdf["labels"].apply(old2new_labels)
    gdf["original_split"] = gdf["name"].apply(get_original_split_from_patch_name)
    gdf = assign_to_ben_country(gdf)
    gdf["season"] = tfm_month_to_season(gdf["acquisition_date"])
    return gdf


# Cell
def _remove_snow_cloud_patches(gdf):
    snowy = gdf["name"].apply(is_snowy_patch)
    cloudy = gdf["name"].apply(is_cloudy_shadowy_patch)
    return gdf[~(snowy | cloudy)]


def remove_bad_ben_gdf_entries(gdf: geopandas.GeoDataFrame) -> geopandas.GeoDataFrame:
    """
    It will ensure that the returned frame will only contain patches that
    also have labels for the 19 label version.

    If the GeoDataFrame doesn't include a column named `new_labels`, it
    will be created by converting the `labels` column.
    The patches that do not contain any `new_labels` are dropped.

    There are 57 patches that would have no target labels.
    Also patches that are covered by seasonal snow or clouds/shadows
    are removed if present.

    The dataframe will be reindexed.
    """
    gdf["new_labels"] = gdf["labels"].apply(old2new_labels)
    errs = gdf["new_labels"].isna()
    gdf.drop(gdf[errs].index, inplace=True)  # remove wrong elements
    gdf = _remove_snow_cloud_patches(gdf)
    gdf = gdf.reset_index(drop=True)
    return gdf


# Cell
import shutil
import tempfile


def build_raw_ben_parquet(
    ben_path: Path,
    output_path: Path = Path() / "raw_ben_gdf.parquet",
    n_workers: int = 8,
    target_proj: str = "epsg:4326",
    verbose: bool = True,
) -> Path:
    """
    Create a fresh BigEarthNet-style parquet file
    from all the image patches in the root `ben_path` folder.
    The output will be written to `output_path`.

    The default output is `raw_ben_gdf` in the current directory.

    The other options are only for advanced use.
    Returns the resolved output path.
    """
    output_path = output_path.resolve()
    gdf = get_gdf_from_patch_dir(ben_path, n_workers=n_workers, target_proj=target_proj)
    gdf.to_parquet(output_path)
    if verbose:
        rich.print(f"[green]Output written to:\n {output_path}[/green]")
    return output_path


def extend_ben_parquet(
    ben_parquet_path: Path,
    output_name: str = "extended_ben_gdf.parquet",
    verbose: bool = True,
) -> Path:
    """
    Extend an existing BigEarthNet-style parquet file.

    The output will be written next to `ben_parquet_path` with the file
    `output_name`.
    The default name is `extended_ben_gdf`.

    This function heavily relies on the structure of the parquet file.
    It should only be used on parquet files that were build with this library!
    Use the functions of this package directly to have more control!
    """
    path = ben_parquet_path.resolve(strict=True)
    gdf = geopandas.read_parquet(path)
    extended_gdf = add_full_ben_metadata(gdf)
    output_path = path.with_name(output_name)
    extended_gdf.to_parquet(output_path)
    if verbose:
        rich.print(f"[green]Output written to:\n {output_path}[/green]")
    return output_path


def remove_discouraged_parquet_entries(
    ben_parquet_path: Path,
    output_name: str = "cleaned_ben_gdf.parquet",
    verbose: bool = True,
) -> Path:
    """
    Remove entries of an existing BigEarthNet-style parquet file.

    The output will be written next to `ben_parquet_path` with the file
    `output_name`.
    The default name is `cleaned_ben_gdf.parquet`.

    This function only requires the input parquet file to have the
    `name` column and the original 43-class nomenclature called `labels`.
    """
    path = ben_parquet_path.resolve(strict=True)
    gdf = geopandas.read_parquet(path)
    cleaned_gdf = remove_bad_ben_gdf_entries(gdf)
    output_path = path.with_name(output_name)
    cleaned_gdf.to_parquet(output_path)
    if verbose:
        rich.print(f"[green]Output written to:\n {output_path}[/green]")
    return output_path


@fc.delegates(build_raw_ben_parquet, but=["output_path"])
def build_recommended_parquet(
    ben_path: Path,
    add_metadata: bool = True,
    output_path: Path = "final_ben.parquet",
    **kwargs,
) -> Path:
    """
    ! Generate the recommended GeoDataFrame and save
    it as a parquet file.

    It will call `build_raw_ben_parquet` under the hood and remove
    patches that are not recommended for DL.
    If `add_metadata` is set, the GeoDataFrame will be
    enriched with extra information, such as Country and Season of the patch.
    See `add_full_ben_metadata` for more information.

    This tool will store all intermediate results in a temporary directory.
    This temporary directory will be printed to allow accessing these
    intermediate results if necessary.
    The resulting GeoDataFrame will be copied to `output_path`.

    The other keyword arguments should usually be left untouched.
    """
    output_path = Path(output_path).resolve()
    tmp_dir_fp = tempfile.TemporaryDirectory()
    tmp_dir = Path(tmp_dir_fp.name)
    rich.print("[yellow]The intermediate results will be stored in: [/yellow]")
    rich.print(f"[yellow]{tmp_dir}[/yellow]\n\n")

    rich.print("Parsing from json files")
    rich.print("This may take up to 30min for the entire dataset!")
    raw_gdf_path = build_raw_ben_parquet(
        ben_path, output_path=tmp_dir / "raw_ben_gdf.parquet", **kwargs
    )

    rich.print("Removing discouraged entries")
    gdf_path = remove_discouraged_parquet_entries(raw_gdf_path)

    if add_metadata:
        rich.print("Adding metadata")
        gdf_path = extend_ben_parquet(gdf_path)

    shutil.copyfile(gdf_path, output_path)
    rich.print(f"Final result copied to {output_path}")
    return output_path


# Cell

def _run_gdf_cli() -> None:
    app = typer.Typer()
    # hack command registration here
    # to better test the underlying function
    app.command()(build_recommended_parquet)
    app.command()(build_raw_ben_parquet)
    app.command()(remove_discouraged_parquet_entries)
    app.command()(extend_ben_parquet)
    app()

if __name__ == "__main__" and not fc.IN_IPYTHON:
    _run_gdf_cli()
