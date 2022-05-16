import tarfile
from enum import Enum
from importlib import resources
from pathlib import Path

import appdirs
from pydantic import DirectoryPath, validate_arguments

import bigearthnet_common


class ExampleResource(str, Enum):
    s1_example_bz2_tar = "BigEarthNet-S1-Example.tar.bz2"
    s2_example_bz2_tar = "BigEarthNet-S2-Example.tar.bz2"

    def __str__(self):
        return self.value


USER_DIR = Path(appdirs.user_data_dir("bigearthnet_common"))
USER_DIR.mkdir(exist_ok=True, parents=True)


@validate_arguments
def _extract_sentinel_resource(
    resource: ExampleResource,
    subfolder_name: str,
    target_root_dir: DirectoryPath = USER_DIR,
) -> Path:
    """
    Given a local `resource` (one of `ExampleResource`), extract the `subfolder_name` of the compressed
    tar file to the given `target_root_directory`.
    The output path will be `<target_root_dir>/<subfolder_name>`
    Where `subfolder_name` _must_ be a root-folder of the compressed archive!

    The archive will _always_ be extracted. The function applies no caching!
    """
    extracted_dir = target_root_dir / subfolder_name

    if not resources.is_resource(bigearthnet_common, resource):
        raise ValueError(
            f"{resource} resource is not available! This means that it was forgotten to be packaged."
        )
    with resources.path(bigearthnet_common, resource) as resource_path:
        tar_file = tarfile.open(resource_path)
        folder_dir = tar_file.getnames()[0]
        assert folder_dir == subfolder_name
        tar_file.extractall(target_root_dir)
    assert extracted_dir.exists()
    return extracted_dir


def get_s1_example_folder_path() -> Path:
    """Get the path to a tiny subset of BigEarthNet-S1"""
    resource = ExampleResource.s1_example_bz2_tar
    subfolder = "BigEarthNet-S1-Example"
    return _extract_sentinel_resource(resource, subfolder)


def get_s2_example_folder_path() -> Path:
    """Get the path to a tiny subset of BigEarthNet-S2"""
    resource = ExampleResource.s2_example_bz2_tar
    subfolder = "BigEarthNet-S2-Example"
    return _extract_sentinel_resource(resource, subfolder)


def get_s1_example_patch_path() -> Path:
    """Get the path to a single BigEarthNet-S1 patch."""
    s1_dir = get_s1_example_folder_path()
    return sorted(p for p in s1_dir.iterdir())[0]


def get_s2_example_patch_path() -> Path:
    """Get the path to a single BigEarthNet-S2 patch."""
    s2_dir = get_s2_example_folder_path()
    return sorted(p for p in s2_dir.iterdir())[0]
