# allow docker image to overwrite the environment
env-name := env_var_or_default("MAMBA_ENV_NAME", "bigearthnet_common")


env-cmd := "poetry run"
set dotenv-load := false

install: install_python_deps install_ipykernel

install_python_deps:
    poetry install

install_ipykernel:
	{{env-cmd}} python -m ipykernel install --user --name {{env-name}}

build: install_ipykernel
	{{env-cmd}} sphinx-build {{justfile_directory()}}/docs {{justfile_directory()}}/docs/_build/

# Serve docs by calling serve_docs.py function
serve-docs: build
	{{env-cmd}} python {{justfile_directory()}}/serve_docs.py

# Serve docs by callling sphinx-autobuild (works better for sphinx-template work)
serve-docs-autobuild:
	{{env-cmd}} sphinx-autobuild {{justfile_directory()}}/docs {{justfile_directory()}}/docs/_build --open-browser

test:
	{{env-cmd}} pytest tests/

# Run CMDS in the generated environment
run +CMDS:
	{{env-cmd}} {{CMDS}}
