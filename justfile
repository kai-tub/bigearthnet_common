env := "ben_common_env"
min_python := "3.7" # only used for poetry install!

install: install-requirements
	mamba run --prefix {{justfile_directory()}}/{{env}} python -c "import geopandas; print('geopandas is loaded')"
	mamba run --prefix {{justfile_directory()}}/{{env}} python -m ipykernel install --user

install-requirements:
	mamba env create --prefix ./{{env}} -f env.yml --force

install_poetry:
	mamba create --prefix {{justfile_directory()}}/{{env}} python={{min_python}} --force
	mamba run --prefix {{justfile_directory()}}/{{env}} poetry install
	mamba run --prefix {{justfile_directory()}}/{{env}} python -m ipykernel install --user
	# dependencies to view documentation locally
	mamba run --prefix {{justfile_directory()}}/{{env}} mamba install -c conda-forge docker-compose

docs:
	docker-compose up
