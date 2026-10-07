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
| `FLASK_DEBUG` | `False` | Set to `True` to enable the Flask debugger |
| `DATABASE_URI` | Absolute path to `instance/trip_planner.db` | Database connection string |

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
│   ├── __init__.py
│   ├── config/
│   │   └── config.py
│   ├── data/
│   │   └── constants.py
│   ├── models/
│   │   └── trip.py
│   ├── routes/
│   │   ├── health.py
│   │   └── trip.py
│   ├── services/
│   │   └── trip.py
│   └── utils/
│       ├── error_util.py
│       ├── extension_util.py
│       └── validation_util.py
└── instance/
    └── trip_planner.db
```


## API endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Application health |
| POST | `/api/v1/trips` | Create a trip |
| GET | `/api/v1/trips` | List trips |
| GET | `/api/v1/trips/<trip_id>` | Get one trip |
| PUT | `/api/v1/trips/<trip_id>` | Update a trip |
| DELETE | `/api/v1/trips/<trip_id>` | Delete a trip |
| POST | `/api/v1/trips/<trip_id>/travelers` | Add a traveler to a trip |
| DELETE | `/api/v1/trips/<trip_id>/travelers/<traveler_id>` | Remove a traveler from a trip |

Remaining endpoints are documented as they are implemented.

## Assumptions

- `PUT /api/v1/trips/<trip_id>` accepts partial payloads. Fields that are
  absent keep their current values.
- `PUT` ignores a `status` field in the body. Status changes go through
  `PATCH /api/v1/trips/<trip_id>/status` so that lifecycle rules cannot be
  bypassed.
- `GET /api/v1/trips` returns a JSON array of trip objects.
- A request body that is missing, malformed, or not sent as
  `application/json` is rejected with HTTP 400.
- Travelers are global records identified by email. Adding a traveler whose
  email already exists reuses the existing record instead of creating a
  duplicate. Emails are compared after trimming and lowercasing.
- A traveler's stored name is not updated when the same email is added to a
  later trip.
- BR-06 is applied to every trip a traveler participates in, regardless of
  that trip's status, because the rule states no exception. A CANCELLED trip
  therefore still blocks an overlapping one.
- Two date ranges are treated as overlapping when neither ends strictly
  before the other begins, so a trip ending on the same day another begins
  is a conflict.
- Removing a traveler is allowed while a trip is PLANNED or ONGOING, and
  rejected for COMPLETED and CANCELLED trips, which cannot be edited
  (BR-12, BR-13).
- Removing a traveler from a trip deletes the participation only. The
  traveler record remains and may belong to other trips.
- Deleting a trip also deletes its participations and expenses.
- Reducing `max_travelers` below the current traveler count returns HTTP 409.