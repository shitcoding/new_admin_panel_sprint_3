# Useful command to display all available Makefile commands with `make help`
help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

#-----------------------------------------------------------------------------
# Creating .env files to store credentials for Docker containers

DOTENVS_PATH := ./docker_compose/.envs
ENVS := dev prod
SERVICES := db django

dotenv: ## Create .env files (if they don't exist) from template .env.example files
	@created=0; \
	echo "Creating .env files in $(DOTENVS_PATH)"; \
	for env in $(ENVS); do \
		dotenv_dir="$(DOTENVS_PATH)/.$$env"; \
		for service in $(SERVICES); do \
			env_file="$$dotenv_dir/.$$service"; \
			if [ ! -f "$$env_file" ]; then cp "$$env_file.example" "$$env_file"; \
				echo "Created: $$env_file"; \
				created=1; \
			fi; \
		done; \
	done; \
	if [ $$created -eq 0 ]; then \
		echo ".env files already exist, no new files created"; \
	else \
		echo ".env files created successfully in $(DOTENVS_PATH). Don't forget to change credentials!"; \
	fi

#-----------------------------------------------------------------------------
# Starting up project containers with docker-compose

dev-docker-up:	## Start containers in dev mode
	@docker-compose -f ./docker_compose/docker-compose.dev.yml up -d --build

dev-docker-down:	## Stop containers and remove volumes in dev mode
	@docker-compose -f ./docker_compose/docker-compose.dev.yml down -v

prod-docker-up:	## Start containers in production mode
	@docker-compose -f ./docker_compose/docker-compose.prod.yml up -d --build

prod-docker-down:	## Stop containers and remove volumes in production mode
	@docker-compose -f ./docker_compose/docker-compose.prod.yml down -v


#-----------------------------------------------------------------------------
django-superuser:	## Create django superuser
	@docker exec -it movies-admin-app make superuser-docker

dummy-django-superuser:	## Autocreate test django superuser with predefined login/pass
	@docker exec movies-admin-app make dummy-superuser-docker



#-----------------------------------------------------------------------------
.PHONY: \
	help \
	dotenv \
	dev-docker-up \
	dev-docker-down \
	prod-docker-up \
	prod-docker-down \
	dummy-django-superuser \
