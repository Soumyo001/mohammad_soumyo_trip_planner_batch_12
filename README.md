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
│   │   ├── trip.py
│   │   ├── traveler.py
│   │   ├── trip_traveler.py
│   │   └── expense.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── trip.py
│   │   ├── traveler.py
│   │   └── expense.py
│   ├── services/
│   │   ├── trip.py
│   │   ├── traveler.py
│   │   └── expense.py
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
| POST | `/api/v1/trips/<trip_id>/expenses` | Add an expense to a trip |
| GET | `/api/v1/trips/<trip_id>/summary` | Calculated trip summary |
| PATCH | `/api/v1/trips/<trip_id>/status` | Change trip status |

## Example requests and responses

### Create a trip

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips \
  -H "Content-Type: application/json" \
  -d '{"destination":"Coxs Bazar","start_date":"2026-10-20","end_date":"2026-10-23","budget":30000,"max_travelers":5}'
```

`201 Created`

```json
{
  "id": 1,
  "destination": "Coxs Bazar",
  "start_date": "2026-10-20",
  "end_date": "2026-10-23",
  "budget": 30000.0,
  "max_travelers": 5,
  "status": "PLANNED"
}
```

### Add a traveler

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/travelers \
  -H "Content-Type: application/json" \
  -d '{"name":"Ayesha Rahman","email":"ayesha@example.com"}'
```

`201 Created`

```json
{
  "id": 1,
  "name": "Ayesha Rahman",
  "email": "ayesha@example.com"
}
```

### Add an expense

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/expenses \
  -H "Content-Type: application/json" \
  -d '{"title":"Hotel","amount":12000}'
```

`201 Created`

```json
{
  "id": 1,
  "trip_id": 1,
  "title": "Hotel",
  "amount": 12000.0
}
```

### Change trip status

```bash
curl -X PATCH http://127.0.0.1:5000/api/v1/trips/1/status \
  -H "Content-Type: application/json" \
  -d '{"status":"ONGOING"}'
```

`200 OK` — the updated trip object, with `status` set to `ONGOING`.

### Trip summary

```bash
curl http://127.0.0.1:5000/api/v1/trips/1/summary
```

`200 OK`

```json
{
  "trip_id": 1,
  "destination": "Coxs Bazar",
  "status": "ONGOING",
  "budget": 30000.0,
  "max_travelers": 5,
  "traveler_count": 1,
  "available_seats": 4,
  "total_expense": 12000.0,
  "remaining_budget": 18000.0
}
```

### Error response

Every failure returns the same shape.

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/travelers \
  -H "Content-Type: application/json" \
  -d '{"name":"Ayesha Rahman","email":"ayesha@example.com"}'
```

`409 Conflict`

```json
{
  "error": "DUPLICATE_TRAVELER",
  "message": "Traveler ayesha@example.com is already a part of this trip"
}
```

## Business rules

| Rule | Requirement | Enforced in | Failure |
|------|-------------|-------------|---------|
| BR-01 | `end_date` later than `start_date` | `validate_date_order` in `app/utils/validation_util.py` | 400 |
| BR-02 | `budget` greater than zero | `parse_positive_number` in `app/utils/validation_util.py` | 400 |
| BR-03 | `max_travelers` greater than zero | `parse_positive_integer` in `app/utils/validation_util.py` | 400 |
| BR-04 | No duplicate traveler on a trip, identified by email | `ensure_traveler_not_in_this_trip` in `app/services/traveler.py`, plus a unique constraint on `trip_travelers` | 409 |
| BR-05 | Traveler count never exceeds `max_travelers` | `ensure_trip_has_free_seat` in `app/services/traveler.py` | 409 |
| BR-06 | No traveler in two overlapping trips | `ensure_no_overlapping_trip` in `app/services/traveler.py` | 409 |
| BR-07 | Expense amount greater than zero | `parse_positive_number` in `app/utils/validation_util.py` | 400 |
| BR-08 | Total expenses never exceed the budget | `ensure_expense_fits_budget` in `app/services/expense.py` | 409 |
| BR-09 | `max_travelers` not reduced below traveler count | `ensure_capacity_fits_current_travelers` in `app/services/trip.py` | 409 |
| BR-10 | Travelers added only while PLANNED | `ensure_trip_accepts_travelers` in `app/services/traveler.py` | 409 |
| BR-11 | Expenses added only while PLANNED or ONGOING | `ensure_trip_accepts_expenses` in `app/services/expense.py` | 409 |
| BR-12 | COMPLETED trips are frozen | `ensure_trip_is_editable` in `app/services/trip.py`, `TripStatus.TERMINAL` and `ALLOWED_TRANSITIONS` in `app/data/constants.py` | 409 |
| BR-13 | CANCELLED trips are frozen | Same as BR-12 | 409 |
| BR-14 | Only the defined lifecycle transitions are valid | `TripStatus.ALLOWED_TRANSITIONS` in `app/data/constants.py`, checked by `ensure_transition_is_allowed` | 409 |

> The lifecycle is defined as data rather than conditional branches, so a
change to the permitted transitions is a change to a single dictionary in
`app/data/constants.py`.

## Assumptions

- `PUT /api/v1/trips/<trip_id>` accepts partial payloads. Fields that are
  absent keep their current values.
- `PUT` ignores a `status` field in the body. Status changes go through
  `PATCH /api/v1/trips/<trip_id>/status` so that lifecycle rules cannot be
  bypassed.
- `GET /api/v1/trips` returns a JSON array of trip objects.
- A request body that is missing, malformed or not sent as
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
- Removing a traveler is allowed while a trip is PLANNED or ONGOING and
  rejected for COMPLETED and CANCELLED trips, which cannot be edited
  (BR-12, BR-13).
- Removing a traveler from a trip deletes the participation only. The
  traveler record remains and may belong to other trips.
- Deleting a trip also deletes its participations and expenses.
- Reducing `max_travelers` below the current traveler count returns HTTP 409.
- Email addresses are validated against a standard pattern requiring a
  domain with a top-level domain, so addresses such as `user@localhost` are
  rejected.
- Money comparisons are rounded to two decimal places so that an expense
  exactly equal to the remaining budget is accepted (BR-08), without
  floating point representation error causing a false rejection.
- The summary endpoint is read-only and available in every trip status.
- `total_expense` is 0 and `remaining_budget` equals the budget for a trip
  with no expenses.
- A `status` value that is not one of the four lifecycle states is rejected
  with HTTP 400 as invalid input. A valid state that is not a permitted
  transition from the current state is rejected with HTTP 409.
- Status values are accepted case-insensitively and stored in uppercase.
- A transition to the trip's current status is rejected, since it is not
  one of the transitions defined in the assignment.
- `PUT` is rejected for COMPLETED and CANCELLED trips (BR-12, BR-13) and
  allowed for PLANNED and ONGOING trips.
- `DELETE` is permitted in any status. BR-12 and BR-13 restrict editing a
  trip and deleting is not an edit.

## Known limitations

- Monetary values are stored as floating point numbers. Comparisons are
  rounded to two decimal places to keep budget checks exact, but a
  production system would store amounts as integer minor units or use a
  decimal column type.
- Changing a trip's dates through `PUT` does not re-check BR-06 for
  travelers who already joined. A date change can therefore create an
  overlap that would have been rejected at join time. The assignment
  specifies BR-06 only for the join operation.
- Business rules are checked and then committed as separate steps, so two
  simultaneous requests could in principle both pass a capacity or budget
  check. The unique constraint on `trip_travelers` prevents duplicate
  participation at the database level; the other rules rely on the
  single-process development server used for this assignment.
- `GET /api/v1/trips` returns every trip with no pagination or filtering.
- Tables are created with `db.create_all()`. There is no migration tooling,
  so a change to a model requires recreating the database file.
- A traveler record remains after being removed from every trip, since
  travelers are global entities identified by email.
- Authentication and authorization are out of scope, so any client can
  modify any trip.