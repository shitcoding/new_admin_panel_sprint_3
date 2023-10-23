# Useful command to display all available Makefile commands with `make help`
help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

#-----------------------------------------------------------------------------
# Utility commands

wheels:  # Build wheels with/without dev dependencies (used for building Docker containers)
ifeq (${MODE}, dev)
	pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements-dev.txt
else ifeq ($(filter ${MODE}, prod),${MODE})
	pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
else
	@echo "Error: MODE env variable not set properly. Please set MODE to 'dev' or 'prod'."
	@exit 1
endif

wait-postgres:  # Helper command to wait for postgres server or container to start up
	python3 ./utils/wait_for_postgres.py



#-----------------------------------------------------------------------------
# Setting up the app

install: ## Create venv and install app dependencies via poetry (to run app locally)
	@poetry install --no-root

migrate: ## Apply django migrations
	@poetry run python3 manage.py migrate --fake movies 0001
	@poetry run python3 manage.py migrate

migrate-docker: ## Apply django migrations (when running app in Docker)
	@python3 manage.py migrate --fake movies 0001
	@python3 manage.py migrate

makemigrations: ## Create new migrations if required
	@poetry run python3 manage.py makemigrations

superuser: ## Create django superuser
	@poetry run python3 manage.py createsuperuser

superuser-docker: ## Create django superuser (when running app in Docker)
	@python3 manage.py createsuperuser

dummy-superuser: ## Autocreate test superuser with predefined login/pass
	@DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=wow-so-secret \
	DJANGO_SUPERUSER_EMAIL=mail@mail.kek \
	poetry run python3 manage.py createsuperuser --noinput || true && \
	echo "Test Django superuser login/pass: admin / wow-so-secret"

dummy-superuser-docker: ## Autocreate test superuser (when running app in Docker)
	@DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=wow-so-secret \
	DJANGO_SUPERUSER_EMAIL=mail@mail.kek \
	python3 manage.py createsuperuser --noinput || true && \
	echo "Test Django superuser login/pass: admin / wow-so-secret"

translation: ## Prepare files for translation
	@poetry run django-admin makemessages -i "venv" -i ".venv" -l en -l ru

compile-translation: ## Compile translation
	@poetry run django-admin compilemessages -i "venv" -i ".venv" -l en -l ru

# Static files management
# ------------------------------------------------------------------------------
collectstatic:  ## Collect static files (when running app locally) 
	@poetry run python3 manage.py collectstatic --no-input

collectstatic-docker:  ## Collect static files  (when running app in Docker)
	python3 manage.py collectstatic --no-input

#-----------------------------------------------------------------------------
# Running the app server

run-dev-server:	## Run django dev server
	@poetry run python3 manage.py runserver

run-dev-server-docker: \
	wait-postgres \
	migrate-docker	\
	collectstatic-docker ## Run django dev server (when running app in Docker)

	@python3 manage.py runserver 0.0.0.0:8000

run-gunicorn-docker: \
	wait-postgres \
	migrate-docker \
	collectstatic-docker 	## Run Gunicorn server (when running app in Docker)

	@python3 -m gunicorn config.wsgi:application --bind 0.0.0.0:8000


#-----------------------------------------------------------------------------
.PHONY: \
	help \
	wheels \
	wait-postgres \
	dotenv \
	install \
	migrate \
	migrate-docker \
	makemigrations \
	superuser \
	superuser-docker \
	dummy-superuser \
	dummy-superuser-docker \
	translation \
	compile-translation \
	run-dev-server \
	run-dev-server-docker \
