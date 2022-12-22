.DEFAULT_GOAL:=help

COMPOSE_ALL := -f docker-compose.yml # Add more services
COMPOSE_FARM := -f docker-compose.yml
SERVICES := client server
CLIENT_SERVICES := client
SERVER_SERVICES := server

#----------- Check Docker Support ----------#

compose_v2_not_supported = $(shell command docker compose 2> /dev/null)
ifeq (,$(compose_v2_not_supported))
  DOCKER_COMPOSE_COMMAND = docker-compose
else
  DOCKER_COMPOSE_COMMAND = docker compose
endif

#----------- Routines --------------------#
.PHONY: client server all down stop restart rm logs prune help

all:			## Start all services
	$(DOCKER_COMPOSE_COMMAND) up -d --build

client:			## Start the client container
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE_FARM} up -d --build ${CLIENT_SERVICES}

server:			## Start the server container
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE_FARM} up -d --build ${SERVER_SERVICES}

ps:				## Show all containers
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE_ALL} ps
down:			## Down containers
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE_ALL} down

stop:			## Stop containers
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE_ALL} stop $(SERVICES)

restart:		## Restart Containers
	$(DOCKER_COMPOSE_COMMAND) ${COMPOSE_ALL} restart $(SERVICES)

rm:				## Remove containers
	$(DOCKER_COMPOSE_COMMAND) $(COMPOSE_ALL) rm -f ${SERVICES}

logs:			## Tail all container logs
	$(DOCKER_COMPOSE_COMMAND) $(COMPOSE_ALL) logs --follow --tail=1000 ${SERVICES}

prune:			## Remove containers and delete volumes
	@make stop && make rm
	@docker volume prune -f --filter label=com.docker.compose.project=animalfarm


help:       	## Show this help.
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m (default: help)\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)