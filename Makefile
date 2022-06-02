S3_BUCKET="ece229-dataset"

all: local-deploy

deploy:
	bash scripts/deploy.sh

run-development-server: local-deploy
	pipenv run python -m carsreco

run-server: local-deploy
	pipenv run gunicorn

local-deploy: get-data deps

install-unit: scripts/carsreco.service
	cp $< /etc/systemd/system/

deps: Pipfile
	pipenv install

dev-deps: Pipfile
	pipenv install --dev



#---------------------------------------------------------------
#Others
#---------------------------------------------------------------
	
get-data: data/preprocessed.csv

data/: 
	mkdir -p data

data/vehicles_cleaned_imputed.csv: data/
	aws s3 cp  s3://$(S3_BUCKET)/vehicles_cleaned_imputed.csv data/vehicles_cleaned_imputed.csv

data/preprocessed.csv: data/vehicles_cleaned_imputed.csv data/ deps
	pipenv run python scripts/preprocessing.py $< $@


#-----------------------------------------------------------
# Documentation
# ---------------------------------------------------------

docgen: docs dev-deps
	pipenv run  $(MAKE) -C docs html

docs: docs-dir autodoc docs/source/README.md nbconvert

docs-dir: staticdocs
	cp -Rf staticdocs docs

autodoc: docs-dir dev-deps
	pipenv run sphinx-apidoc -f -e -o docs/source scripts
	pipenv run sphinx-apidoc -f -e -o docs/source carsreco

docs/source/README.md: docs-dir
	cp ./README.md docs/source/README.md


nbconvert: docs-dir dev-deps
# 	pipenv run jupyter-nbconvert --to rst tests/Process.ipynb  --output-dir ./docs/source
# 	sed -i "/^\s*INFO:/d" ./docs/source/Process.rst #remove the innumerable INFO: lines
#

#---------------------------------------------------------------
#Others
#---------------------------------------------------------------


# install-kernel: deps
# 	pipenv run python -m ipykernel install --user --name=ECE143-project-env

clean:
	rm -rf docs

.PHONY: clean docs docs-dir autodoc nbconvert docgen local-deploy run-server
