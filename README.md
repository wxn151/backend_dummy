# Demo App (with auth)

A back end built with FastAPI and PostgreSQL to demonstrate how to build a full-stack web application using modern web technologies.

Project demo: https://behemoth-backend.onrender.com/

## Features

- It allows to user registration, validate mail and recover password (smtp server).
- Schemas implemented to validate input and output data
- JWT and OAuth2 implementation.
- JWT and OAuth2 implementation.
- Migration to db with Alembic

## Getting started: Without Docker

a) Clone repository into your machine

```md
git clone https://github.com/wxn151/backend_dummy.git
```

b) Create a virtual environment

<details>
<summary>Steps</summary>
1. Creating a virtual environment

```md
python3 -m venv venv
or python -m venv venv (on windows) 
```

2.Activating it

```md
source venv/bin/activate
or .\venv\Scripts\activate (on windows)
```
</details>


c) Installing dependencies

```md
pip install -r requirements.txt
```

d) Create .env file
```md
TITLE = your_title_app
DESCRIPTION = your_description_app
DATABASE_URL = your_db_connection 
SECRET_KEY = your_secret_key
MAIL = your_smtp_mail_address
PASSWORD = your_smtp_password
ALGORITHM = your_encryption_algorithm # suggest HS256
SAAS_LINK = your_front_end_link
```

e) Migrate with help of Alembic

###### Linux
```md
alembic revision --autogenerate -m "initial"
alembic upgrade head
```
###### Windows
```md
python -m alembic revision --autogenerate -m "initial"
python -m alembic upgrade head
```

f) Run app

```md
uvicorn backend.main:app --host 0.0.0.0 --port 8000 
```

## Getting started: With Docker

a) Start
```md
docker compose -f .\docker-compose-dev.yml up -d
```

b) Stop
```md
docker compose -f .\docker-compose-dev.yml down
```

## Documentation
1. Swagger UI

    ```linux
    http://localhost:8000/docs
    ```
2. Redocly

    ```linux
    http://localhost:8000/redoc
    ```

## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 file for details.
