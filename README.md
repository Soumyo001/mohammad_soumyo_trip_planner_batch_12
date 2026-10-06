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
├── app/
│   ├── init.py
│   ├── config.py
│   ├── extensions.py
│   ├── errors.py
│   ├── models.py
│   └── routes.py
└── instance/
    └── trip_planner.db
```


## API endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Application health |

Remaining endpoints are documented as they are implemented.