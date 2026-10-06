# Smart Group Trip Planner API

A REST API for managing group trips, travelers, expenses and trip lifecycle
rules, built with Python, Flask and SQLite.

## Problem statement

A travel organization needs a backend service to manage group trips. A trip
has a destination, date range, budget, capacity, travelers, expenses and a
lifecycle status. The API prevents invalid operations such as overbooking,
duplicate participation, overlapping trips for the same traveler,
overspending and invalid status transitions.

## Prerequisites

- Python 3.10 or newer
- bash (to run `./run.sh`)

## Run from a fresh clone

```bash
./run.sh
```

The API starts on http://127.0.0.1:5000

If the script is not executable:

```bash
chmod +x run.sh
./run.sh
```

## Manual run

```bash
pip install -r requirements.txt
python run.py
```

## Environment variables

The repository ships a `.env.example` file. `./run.sh` copies it to `.env`
on first run. When running manually, copy it yourself:

```bash
cp .env.example .env
```

All variables have safe defaults in the application, so the API starts
correctly even if `.env` is missing.

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_HOST` | `127.0.0.1` | Host the server binds to |
| `FLASK_PORT` | `5000` | Port the server listens on |
| `FLASK_DEBUG` | `0` | Set to `1` to enable the Flask debugger |
| `DATABASE_URI` | `sqlite:///instance/trip_planner.db` | Database connection string |

> `DATABASE_URI` may be left empty. If you set it to a SQLite file, use an
absolute path - Flask-SQLAlchemy resolves relative SQLite paths against the
instance folder.

## How SQLite is initialized and stored

The database file is created at `instance/trip_planner.db` the first time the
application starts. `db.create_all()` runs inside the application factory, so
no manual SQL or configuration is needed. The file is generated locally and is
not committed to the repository.

## Project structure

```bash
.
├── run.py 
├── run.sh 
├── requirements.txt 
├── README.md
├── .gitignore
├── .env.example 
├── app/
│ ├── init.py
│ ├── config/
│ │ └── config.py
│ ├── data/
│ │ └── constants.py
│ ├── models/
│ │ └── trip.py
│ ├── routes/
│ │ ├── init.py
│ │ └── health.py
│ ├── services/
│ └── utils/
│   ├── error_util.py
│   └── extension_util.py
└── instance/
    └── trip_planner.db
```


## API endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Application health |

Remaining endpoints are documented as they are implemented.