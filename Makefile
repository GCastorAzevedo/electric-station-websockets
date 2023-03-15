PORT=65432

check:
	./static_checks.sh

sockets:
	netstat -an | grep ${PORT}

pids:
	lsof -i -n | grep ${PORT}

start-client:
	poetry run python client/start.py

start-server:
	poetry run python server/app/main.py