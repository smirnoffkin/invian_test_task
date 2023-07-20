# Invian test task
#### P.S. A detailed description of the task can be found in [task.pdf](./task.pdf). ####

## Run
### Production

1. `make env`
2. `make up-prod`
3. `make up-tcp-server`
4. `make up-sensor`

### Development

1. `make env`
2. `make dev`
3. `make up-dev`
4. `make migrate`
5. `make run`
6. `make up-tcp-server`
6. `make up-sensor`

Go to `http://localhost:8080/docs` to see open api docs

### Run tests

* `make test`

## Project technology stack

* Python(FastAPI, asyncio, SQLAlchemy, pytest, alembic), PostgreSQL, Redis, Docker
