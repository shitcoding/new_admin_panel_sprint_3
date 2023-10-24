# Useful command to display all available Makefile commands with `make help`
help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

#-----------------------------------------------------------------------------
# Setting up the app

dotenv:  ## Create .env file from template .env.example file
	@test ! -f ./.env && cp ./.env.example ./.env
	@echo ".env file created succesfully. Don't forget to change credentials in it!"

install: dotenv ## Create virtual env and install dependencies via poetry
	@poetry install --no-root


#-----------------------------------------------------------------------------
# Utility commands

reqs:	## Export dependencies without dev deps to requirements.txt
	@poetry export --without-hashes -f requirements.txt -o ./requirements.txt

reqs-dev:	## Export dependencies with dev deps to requirements-dev.txt
	@poetry export --with dev --without-hashes -f requirements.txt -o ./requirements-dev.txt

wheels:  ## Build wheels with/without dev dependencies (used for building Docker containers)
ifeq (${MODE}, dev)
	pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements-dev.txt
else ifeq ($(filter ${MODE}, prod),${MODE})
	pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
else
	@echo "Error: MODE env variable not set properly. Please set MODE to 'dev' or 'prod'."
	@exit 1
endif




#-----------------------------------------------------------------------------
.PHONY: \
	help \
	dotenv \
	install \
	reqs \
	reqs-dev \
