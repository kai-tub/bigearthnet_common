# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/01d_subset_builder.ipynb (unless otherwise specified).

__all__ = ['recurse_link_files']

# Cell
import rich
from pathlib import Path
from typing import List, Optional

# Cell
def recurse_link_files(
    src_dataset, target_dir, only_suffixes: Optional[List[str]] = None
):
    """
    Copy the directory structure of `src_dataset` and
    **link** the files from the `src_dataset` to
    `target_dir`.

    This minimizes the storage-space, while allowing
    to add _local_ files.

    Optionally provide `only_suffixes` to skip all files
    that do **not** have one of the provided extensions.
    These extensions must start with `.`
    """

    for original_patch in paths:
        original_patch.resolve(strict=True)
        if original_patch.is_file():
            continue
        target_patch = target_dir / original_patch.name
        if target_patch.exists():
            rich.print(f"[yellow]Skipping: {target_patch}[/yellow]")
            continue
        target_patch.symlink_to(original_patch, target_is_directory=True)
    return str(target_dir)


# def recurse_link_files(gdf, src_dataset, target_dir):
#     paths = gdf["name"].apply(lambda name: src_dataset / name)
