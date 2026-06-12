# FastAPI Minesweeper

A simple Minesweeper game built using FastAPI, SQLite, HTML, CSS, and JavaScript.

## Features

- Random mine generation
- Cell reveal logic
- SQLite database integration
- FastAPI backend
- Simple web interface

## Project Structure

```
.
├── static/
├── templates/
├── database.py
├── game.py
├── main.py
├── models.py
├── requirements.txt
└── README.md
```

## Installation

### Clone the repository

```bash
git clone https://github.com/sriya020906/minesweeper.git
cd minesweeper
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
uvicorn main:app --reload
```

Open:

http://127.0.0.1:8000

## Database

The SQLite database file (`minesweeper.db`) is excluded from the repository.

Tables are created automatically when the application starts using:

```python
Base.metadata.create_all(bind=engine)
```

A new database file will be generated automatically on first run.

## Technologies Used

- FastAPI
- SQLAlchemy
- SQLite
- HTML
- CSS
- JavaScript
