.PHONY: up

up:
	docker compose -f 'docker-compose.yml' up -d --build  $(c)