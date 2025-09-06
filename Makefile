include .env

.PHONY: up down init psql

##########
# DOCKER #
##########

SERVICES := backend db db-test

# start services
up:
	@make down && docker compose -p ${PROJECT_NAME} up --build --force-recreate $(SERVICES) -d
down:
	@docker compose -p ${PROJECT_NAME} down
init:
	@docker compose rm --stop --force --volumes $(SERVICES) && rm -rf ${DB_STORAGE} && rm -rf ${DB_STORAGE}-test && make up

############
# POSTGRES #
############

# connect to postgres
psql:
	@psql -d postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}