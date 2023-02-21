# resource-api
Simple FastAPI project (not meant for production) to perform CRUD operations on resources:
- GET /resources/
- GET /resources/<resource_id>
- POST /resources/
- PATCH /resources/<resource_id>
- DELETE /resources/<resource_id>

With a simple token based authentication system:
- POST /auth/register
- POST /auth/login
- POST /auth/logout

## Used tools
### Database & Migrations
[Postgres](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) as ORM.
[Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations (being complementary to SQLAlchemy).

### Authentication
The project uses the lib [FastAPI Users](https://fastapi-users.github.io/fastapi-users/) which provides a complete set of authentication/users endpoints, models and schemas.


## How to install?


1. Clone the project

2. Create the .env file in the root folder and use the .env.example as base for its content

3. a. Install with docker (preferred method)

```
docker compose up
```

3. b. Install without docker
- Create the postgres database manually 
- Create a venv:
```
python -m venv pyvenv
```
- Activate it:
```
source pyvenv/bin/activate (on linux)
pyvenv\Scripts\activate.bat (on windows)
```
- Install python libs:
```
pip install -r requirements.txt
```
- Run migrations:
```
alembic upgrade head
```
- Run server:
```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
## How to use?

The API docs should be available at http://127.0.0.1:8001/docs.

Run formatters: `black .` & `isort .`

Run linter: `flake8 .`

Run tests: `pytest`
