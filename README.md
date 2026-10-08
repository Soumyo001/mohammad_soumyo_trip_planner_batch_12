# Smart Group Trip Planner API

This project is a REST API built with Python, Flask, and SQLite. It handles group trips, travelers, expenses, and the rules around a trip's different statuses.

## Problem statement

A travel organization needs a way to manage group trips without having to keep track of everything manually. Each trip has a destination, start and end dates, a budget, a traveler limit, a list of travelers, expenses, and a current status.

The API also checks the rules before making changes. For example, it won't allow more travelers than a trip can hold, add the same traveler twice, put someone on overlapping trips, let expenses go over budget, or accept an invalid status change.

## Prerequisites

You'll need:

- Python 3.10 or newer
- bash (for running `./run.sh`)

## Run from a fresh clone

From the project directory, run:

```bash
./run.sh
```

The API will start at http://127.0.0.1:5000

If you get a permission error because the script isn't executable, run:

```bash
chmod +x run.sh
./run.sh
```

## Manual run

You can also start it manually instead of using the script:

```bash
pip install -r requirements.txt
python run.py
```

## Environment variables

There's a `.env.example` file in the repository. On the first run, `./run.sh` copies it to `.env` automatically. If you're starting the application manually, copy it yourself:

```bash
cp .env.example .env
```

The application has safe defaults for all of these settings, so it can still start if you don't have a `.env` file.

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_HOST` | `127.0.0.1` | Host the server binds to |
| `FLASK_PORT` | `5000` | Port the server listens on |
| `FLASK_DEBUG` | `False` | Set to `True` to enable the Flask debugger |
| `DATABASE_URI` | Absolute path to `instance/trip_planner.db` | Database connection string |

> You can leave `DATABASE_URI` empty. If you set it to a SQLite file, use an absolute path. Flask-SQLAlchemy treats relative SQLite paths as relative to the instance folder.

## How SQLite is initialized and stored

SQLite doesn't need any separate setup here. When the application starts for the first time, it creates the database file at `instance/trip_planner.db`. The application factory calls `db.create_all()`, so there's no need to run SQL or set up the tables manually.

The database file is created on your machine and isn't committed to the repository.

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

These are the available endpoints:

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

Here are a few `curl` examples showing how to use the API and what it returns.

### Create a trip

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips \
  -H "Content-Type: application/json" \
  -d '{"destination":"Coxs Bazar","start_date":"2026-10-20","end_date":"2026-10-23","budget":30000,"max_travelers":5}'
```

Response: `201 Created`

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

Response: `201 Created`

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

Response: `201 Created`

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

Response: `200 OK`. The response contains the updated trip, with its `status` set to `ONGOING`.

### Trip summary

```bash
curl http://127.0.0.1:5000/api/v1/trips/1/summary
```

Response: `200 OK`

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

Errors follow the same JSON format. For example, if you try to add the same traveler to a trip again:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/trips/1/travelers \
  -H "Content-Type: application/json" \
  -d '{"name":"Ayesha Rahman","email":"ayesha@example.com"}'
```

Response: `409 Conflict`

```json
{
  "error": "DUPLICATE_TRAVELER",
  "message": "Traveler ayesha@example.com is already a part of this trip"
}
```

## Business rules

The API checks the following rules when handling requests. I've included where each check happens and the HTTP status returned if it fails.

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

> The allowed status changes are kept in a dictionary in `app/data/constants.py` instead of being scattered across conditional statements. If the transition rules need to change, that dictionary is the only place to update them.

## Assumptions

A few details weren't fully specified, so these are the assumptions used in the implementation:

- `PUT /api/v1/trips/<trip_id>` also works with a partial request body. If a field isn't provided, its existing value stays the same.
- Sending `status` in a `PUT` request won't change the trip status. That has to go through `PATCH /api/v1/trips/<trip_id>/status`, where the lifecycle rules are checked.
- `GET /api/v1/trips` returns a JSON array containing the trips.
- If the request body is missing, contains invalid JSON, or isn't sent as `application/json`, the API returns HTTP 400.
- Travelers are stored as global records and identified by email. If an email is already in the database, the existing traveler record is reused rather than creating another one. Emails are trimmed and converted to lowercase before comparison.
- When an existing traveler is added to another trip using the same email, the name already stored for that traveler stays unchanged.
- BR-06 checks overlapping trips regardless of their status. Since the rule doesn't list exceptions, even a CANCELLED trip can prevent a traveler from joining another trip with overlapping dates.
- Dates are considered overlapping unless one trip ends strictly before the other starts. This means two trips are still considered to overlap if one ends on the same day the other begins.
- A traveler can be removed from a PLANNED or ONGOING trip. Removing someone from a COMPLETED or CANCELLED trip is blocked because those trips can no longer be edited (BR-12 and BR-13).
- Removing someone from a trip only removes their participation in that trip. Their traveler record remains available for other trips.
- Deleting a trip removes its traveler participations and expenses too.
- If `max_travelers` is lowered below the number of people already on a trip, the API responds with HTTP 409.
- Email validation expects a normal domain with a top-level domain. An address such as `user@localhost` won't pass validation.
- For budget checks, monetary values are rounded to two decimal places. This allows an expense equal to the exact remaining budget (BR-08), without a small floating-point difference causing an incorrect rejection.
- The summary endpoint doesn't modify anything and can be used no matter what status the trip is in.
- If a trip has no expenses, `total_expense` is 0 and `remaining_budget` is the same as the original budget.
- An unknown `status` value (anything outside the four lifecycle states) results in HTTP 400. If the status is valid but the transition isn't allowed from the current state, the response is HTTP 409.
- Status values aren't case-sensitive when sent in requests. They're stored in uppercase.
- Setting a trip's status to the status it already has isn't allowed, since that isn't one of the transitions defined in the assignment.
- `PUT` is allowed when a trip is PLANNED or ONGOING, but is rejected when it's COMPLETED or CANCELLED (BR-12 and BR-13).
- `DELETE` is allowed for a trip in any status. BR-12 and BR-13 prevent editing finished trips, but deleting a trip is treated separately from editing it.

## Known limitations

There are some things this version doesn't handle, or that I'd approach differently in a production application:

- Money is currently stored using floating-point numbers. The budget comparisons are rounded to two decimal places, but for production it would be better to use integer minor units or a decimal column type.
- Updating a trip's dates through `PUT` doesn't check BR-06 again for travelers who have already joined. So changing the dates could create an overlap that would have been rejected when the traveler was first added. This follows the assignment, which only requires BR-06 during the join operation.
- The application checks business rules before committing changes. With two requests happening at exactly the same time, both could pass a capacity or budget check. Duplicate participation is protected by a unique constraint on `trip_travelers`, but the other checks depend on the single-process development server used for this assignment.
- `GET /api/v1/trips` returns all trips at once. There's no pagination or filtering yet.
- Database tables are created using `db.create_all()`, without any migration tool. If a model changes, the database file needs to be recreated.
- Travelers are global records, so removing a traveler from all trips doesn't delete that person's record from the database.
- Authentication and authorization aren't included in this project. That means any client can modify any trip.