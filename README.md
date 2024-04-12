# Patreon Clone API

This project is a patreon clone API. It is a work in progress.

## Installation

1. Install the requirements

```sh
pip install -r requirements.txt
```

3. Copy and edit the environment variables in the .env file

```sh
cp .env.example .env
```

> Note: you will need to create a new database before you can edit the postgresql database url in the .env file.

4. Run the migrations

```sh
python manage.py migrate
```

4. Run the server

```sh
python manage.py runserver
```

