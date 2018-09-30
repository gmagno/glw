.PHONY: clean run-api install-ui run-ui test test-last-failed test-serve-report run-log-server docker-compose-build docker-compose-up

#--- SETUP --------------------------------#
include .env
export $(shell sed 's/=.*//' .env)

install: install-ui
	pipenv install --dev && cd ui && npm install

#--- API ----------------------------------#
run-api:
	python app/app.py


#--- UI -----------------------------------#
run-ui:
	cd ui && ./node_modules/local-web-server/bin/cli.js --spa index.html --hostname 0.0.0.0 --port 60030


#--- TEST ---------------------------------#
test:
	pytest test/

test-last-failed:
	pytest -l --lf --tb=short test/

test-serve-report: test
	cd report && python -m http.server 60040


#--- LOG SERVER ---------------------------#
run-log-server:
	python scripts/log_server.py


#--- DOCKER -------------------------------#
docker-compose-build: clean
	docker-compose build --force-rm

docker-compose-up:
	docker-compose up --abort-on-container-exit db adminer app

#--- TEARDOWN -----------------------------#
clean:
	find . \( -name __pycache__ -o -name "*.pyc" -o -name .pytest_cache\
		-o -name htmlcov -o -name report -o -name udp_server.log\
		-o -name glw.log -o -name assets -o -name persistent.db \) -exec rm -rf {} +\
	&& touch compose/log_server/data/udp_server.log\
	&& mkdir -p compose/app/data/report\
	&& touch compose/app/data/report/index.html\
	&& rm -f persistent.db\
	&& docker volume prune
