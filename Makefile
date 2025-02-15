build:
	git pull
	docker compose build

up:
	docker compose up -d

down:
	docker compose down
	docker system prune -f
