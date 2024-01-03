# Santa ERP

## Description

This is a simple ERP system for **Santa Claus**. It is written in Python 3.12` and uses the **FastAPI** with **SQLite**.

## Features

Santa can perform the standard CRUD operations both on Elves and Items. He can also assign both Items and Holidays to Elves.

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

No you can access the app at `http://localhost:8000/`


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
