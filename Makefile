local-db-up:
	docker compose -f docker-compose.yml up --build -d

local-db-down:
	docker compose -f docker-compose.yml stop