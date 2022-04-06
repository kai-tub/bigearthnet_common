# BigEarthNet Set Builder Functions

To quickly build CSV subsets, you can utilize the command:
```sh
ben_build_csv_sets --help
```

To generate a CSV file that contains all Sentinel-2 patches from Serbia only during the Summer and Spring months, call the function as:
- `ben_build_csv_sets <FILE_PATH> S2 --seasons Winter --seasons Summer --countries Serbia --remove-unrecommended-dl-patches`
The tool will ensure that the generated splits are not empty.

You can also use the {mod}`.sets` API directly from your Python application to programmatically generate new splits with more refined control:
- {func}`.filter_patches_by_country`
- {func}`.filter_patches_by_season`
- {func}`.filter_patches_by_split`
