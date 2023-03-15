PORT=65432

check:
	./static_checks.sh

sockets:
	netstat -an | grep ${PORT}

pids:
	lsof -i -n | grep ${PORT}

client:
	python client/main.py

server:
	python server/app/main.py