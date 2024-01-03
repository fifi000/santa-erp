# Santa ERP

## Description

This is a simple ERP system for **Santa Claus**. It is written in `Python 3.12` and uses the **FastAPI** with **SQLite**.

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



## Installation

App was developed using `Python 3.12`

### Virtual Environment

Create a virtual environment with `venv`:

```powershell
python -m venv ./venv
```

Activate the virtual environment:

```bash
source ./venv/bin/activate
```

```powershell
.\.venv\Scripts\activate.ps1
```

### Requirements

```powershell
pip install -r requirements.txt
```

## Run

```powershell
uvicorn main:app --reload
```
