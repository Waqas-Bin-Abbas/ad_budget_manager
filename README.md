# Ad Budget Manager

## Overview

Ad Budget Manager is a FastAPI-based system that manages multiple brands and their advertising campaigns by tracking daily and monthly budgets. It automatically turns off campaigns when budgets are exceeded and supports dayparting to run ads only during specific hours.

## Features

- **Manage multiple brands** with daily and monthly budgets.
- **Turn campaigns on/off** when the budget is exceeded.
- **Reset budgets automatically** at the start of a new day/month.
- **Support dayparting** to control ad schedules.
- **Database migration support** using Alembic.
- **RESTful API** endpoints for managing brands and campaigns.

## Installation & Setup

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd AD_BUDGET_MANAGER
```

### 2. Create a Virtual Environment

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

or

```sh
make venv
```

### 3. Install Dependencies

```sh
make install
```

### 4. Configure Environment Variables

Create a copy of `.env.example` file in the root directory, rename it to `.env` and set the `DATABASE_URL` and `REDIS_URL` in it.

### 5. Run Database Migrations

```sh
make run-migrations
```

### 6. Start the FastAPI Server, celery beat and celery worker.

```sh
make run
```

### 7. API Documentation

After running the server, open the following URL to access API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Assumptions & Simplifications

- The application assumes that campaign status changes take immediate effect.
- The daily and monthly spend resets at midnight UTC.
- Dayparting schedules are checked in real-time before starting an ad.
- Postgreql is used for development.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Commit your changes.
4. Push to your fork and submit a pull request.

## License

This project is licensed under the MIT License.

