# Common BigEarthNet Tools
> A personal collection of common tools to interact with the BigEarthNet dataset.


[![Tests](https://img.shields.io/github/workflow/status/kai-tub/bigearthnet_common/CI?color=dark-green&label=%20Tests)](https://github.com/kai-tub/bigearthnet_common/actions/workflows/main.yml)
[![License](https://img.shields.io/pypi/l/bigearthnet_common?color=dark-green)](https://github.com/kai-tub/bigearthnet_common/blob/main/LICENSE)
[![PyPI version](https://badge.fury.io/py/bigearthnet-common.svg)](https://pypi.org/project/bigearthnet-common/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/bigearthnet-common?color=dark-green)](https://anaconda.org/conda-forge/bigearthnet-common)
[![Auto Release](https://img.shields.io/badge/release-auto.svg?colorA=888888&colorB=9B065A&label=auto&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAACzElEQVR4AYXBW2iVBQAA4O+/nLlLO9NM7JSXasko2ASZMaKyhRKEDH2ohxHVWy6EiIiiLOgiZG9CtdgG0VNQoJEXRogVgZYylI1skiKVITPTTtnv3M7+v8UvnG3M+r7APLIRxStn69qzqeBBrMYyBDiL4SD0VeFmRwtrkrI5IjP0F7rjzrSjvbTqwubiLZffySrhRrSghBJa8EBYY0NyLJt8bDBOtzbEY72TldQ1kRm6otana8JK3/kzN/3V/NBPU6HsNnNlZAz/ukOalb0RBJKeQnykd7LiX5Fp/YXuQlfUuhXbg8Di5GL9jbXFq/tLa86PpxPhAPrwCYaiorS8L/uuPJh1hZFbcR8mewrx0d7JShr3F7pNW4vX0GRakKWVk7taDq7uPvFWw8YkMcPVb+vfvfRZ1i7zqFwjtmFouL72y6C/0L0Ie3GvaQXRyYVB3YZNE32/+A/D9bVLcRB3yw3hkRCdaDUtFl6Ykr20aaLvKoqIXUdbMj6GFzAmdxfWx9iIRrkDr1f27cFONGMUo/gRI/jNbIMYxJOoR1cY0OGaVPb5z9mlKbyJP/EsdmIXvsFmM7Ql42nEblX3xI1BbYbTkXCqRnxUbgzPo4T7sQBNeBG7zbAiDI8nWfZDhQWYCG4PFr+HMBQ6l5VPJybeRyJXwsdYJ/cRnlJV0yB4ZlUYtFQIkMZnst8fRrPcKezHCblz2IInMIkPzbbyb9mW42nWInc2xmE0y61AJ06oGsXL5rcOK1UdCbEXiVwNXsEy/6+EbaiVG8eeEAfxvaoSBnCH61uOD7BS1Ul8ESHBKWxCrdyd6EYNKihgEVrwOAbQruoytuBYIFfAc3gVN6iawhjKyNCEpYhVJXgbOzARyaU4hCtYizq5EI1YgiUoIlT1B7ZjByqmRWYbwtdYjoWoN7+LOIQefIqKawLzK6ID69GGpQgwhhEcwGGUzfEPAiPqsCXadFsAAAAASUVORK5CYII=)](https://github.com/intuit/auto)

This library provides a collection of high-level tools to better work with the [BigEarthNet](bigearth.net) dataset.

`bigearthnet_common` tries to:

1. Collect the most relevant _constants_ into a single place to reduce the time spent looking for these, like:
   - The 19 or 43 class nomenclature strings
   - URL
   - Band statistics (mean/variance) as integer and float
   - Channel names
   - etc.
2. Provide common metadata related functions
   - Safe JSON parser for S1/S2
   - Get the original split
   - Get a list of snowy/cloudy patches
   - Convert the _old_ labels to thew _new_ label nomenclature
   - Generate multi-hot encoded label views

## Installation
The package is available via PyPI and can be installed with:
- `pip install bigearthnet_common`

The package has _Python-only_ dependencies and should cause no issues in more complex Conda environments with various binaries.

## Review constants
To quickly search for BigEarthNet constants of interest, call:
- `ben_constants_prompt` or
- `python -m bigearthnet_common.constants`

## Contributing

Contributions are always welcome!

Please look at the corresponding `ipynb` notebook from the `nbs` folder to review the source code.
These notebooks include extensive documentation, visualizations, and tests.
The automatically generated Python files are available in the `bigearthnet_common` module.

More information is available in the [contributing guidelines](https://github.com/kai-tub/bigearthnet_common/blob/main/.github/CONTRIBUTING.md) document.
