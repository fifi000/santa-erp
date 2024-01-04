# 🧑‍🎄 Santa's ERP

## Description

This is a simple ERP system for **Santa Claus**. It is written in `Python 3.12` and uses the **FastAPI** with **SQLite**.

## Deployment

App is running on [🌊 Digital Ocean](https://www.digitalocean.com/) and can be accessed [here](https://lobster-app-c568d.ondigitalocean.app/).

Docker Image is also available on [🐋 DockerHub](https://hub.docker.com/repository/docker/feefee00/santa-erp/general).

## GitHub Actions

Currently there are two GitHub Actions workflows:

- `python-app.yml` - runs tests and lints the code
- `docker-image.yml` - builds and pushes the Docker image to DockerHub with the `latest` tag

## Features

Santa can perform the standard CRUD operations both on Elves and Items. He can also assign both Items and Holidays to Elves.

### Authentication

User can sign-up and sign-in. Passwords are hashed using `bcrypt`.

In order to register use `/auth/register` endpoint with `POST` method and provide `username` and `password` in the request body.

Remember your `username` and `password` as you will need them to get `JWT token`.

With the `JWT token` you are empowered, like Frodo with the **One Ring** to rule them all, so act wisely. Now you can access additionally:

- `/auth/users/me` - get your user info
- `/auth/time` - get current time

Be aware that `JWT token` expires after 30 minutes.

## Models

``` python
class Elf:
    id: int
    name: str
    items: List[Item]
    holidays: List[Holiday]
```

``` python
class Item:
    id: int
    description: str        
```


## Run with Docker 🐋

Build the image:

```bash
docker-compose build
```

Run the container:

```bash
docker-compose up
```

No you can access the app at `https://localhost:8000/`


## Run without Docker

App was developed using `Python 3.12`

### Virtual Environment

Create a virtual environment with `venv`:

```bash
python -m venv .\.venv
```

Activate the virtual environment:

```bash
# Linux
source ./venv/bin/activate

# Windows
.\.venv\Scripts\activate.ps1
```

### Requirements

```bash
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload
```
