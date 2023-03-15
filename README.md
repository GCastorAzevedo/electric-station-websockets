## Server

Start CSMS server:

```
poetry run python server/app/main.py
```

or

```
make start-server
```

## Server

Start charge point client:

```
poetry run python client/start.py
```

or

```
make start-client
```

## Notes

* Client and Server share dependencies, but the projects could grow separately
into their own repositories or within a monorepo.
* Environment variables are duplicated because client and server packages are treated
as potentially separate projects.
* Poetry and dev dependencies (mypy, lint, isort etc) are shared for convenience
but consider using them separately between server and client.
* Consider packaging the server into a docker image 