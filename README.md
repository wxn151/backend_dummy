# Demo App (with FastAPI)

A basic back end built with FastAPI and Auth to demonstrate how to build a full-stack web application using modern web technologies.

Project demo: https://behemoth-backend.onrender.com/

## Features

- It allows to user registration, sending mail confirmation and recovering password (smtp server).
- JWT and OAuth2 implementation.
- Migration DB (postgres) with Alembic

## Getting started: Without Docker

1. Clone repository into your machine

```md
git clone https://github.com/wxn151/backend_dummy.git
```

2. Create a virtual environment

```bash
python3 -m venv venv
python -m venv venv (on windows) 

# activating it
source venv/bin/activate
.\venv\Scripts\activate (on windows)
```


3. Installing dependencies

```bash
pip install -r requirements.txt
```

4. Create .env file

Create a .env file in the root of your project and add the necessary environment variables.
```md
TITLE = your_title_app
DESCRIPTION = your_description_app
DATABASE_URL = your_db_connection 
SECRET_KEY = your_secret_key
MAIL = your_smtp_mail_address
PASSWORD = your_smtp_password
ALGORITHM = your_encryption_algorithm # suggest HS256
RESET = your_front_end_app
```

5. Migrate with help of Alembic

```md
# linux
alembic revision --autogenerate -m "initial"
alembic upgrade head
```
```md
# windows
python -m alembic revision --autogenerate -m "initial"
python -m alembic upgrade head
```

6. Run app

```md
uvicorn backend.main:app --host 0.0.0.0 --port 8000 
```

## Getting started: With Docker

a) Edit .env file

Add environment variables (including the previous ones).
```md
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
```

a) Start
```md
docker compose -f .\docker-compose-dev.yml up -d
```

b) Stop
```md
docker compose -f .\docker-compose-dev.yml down
```

## Documentation
Swagger UI

    ```linux
    http://localhost:8000/docs
    ```

## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 file for details.
