# Auto scripts

These scripts are used to build the release automatically.
The [auto](https://intuit.github.io/auto/) tool bumps the tag version
and publishes the release on GitHub. The configuration file is the
[.autorc](../.autorc) file in the root project folder. During the
release process, auto will trigger the [update_package_versioning](update_package_versioning.sh)
script. This script replaces the version specification in the `pyproject.toml` file with the
newest release. The previous version is ignored and replaced with the currently published version.

If the version `1.1.2` is currently being published, it will change

```toml
version = "XXX"
```
to
```toml
version = "1.1.2"
```

It will not check what was written between the square brackets.
This aggressive replacement feature makes it robust against accidental manual changes.
