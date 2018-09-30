#/user/bin/env bash
source .env
docker-compose up -d db adminer
sleep 1
docker-compose up -d log_server
sleep 1
docker-compose up -d app
sleep 3
docker-compose up -d ui
sleep 3
docker-compose up -d test

docker-compose logs -f
