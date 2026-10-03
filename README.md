# Deadline Dash Backend

Deadline Dash is a Django REST API for tracking projects, tasks, ownership, progress, and due dates. It includes JWT authentication, PostgreSQL via Docker Compose, and a subscription data foundation for Free, Pro, and Team plans.

## Run with Docker

1. Copy `.env.example` to `.env` and set a strong `DJANGO_SECRET_KEY` and `POSTGRES_PASSWORD`.
2. Start the API and database:

   ```sh
   docker compose up --build
   ```

The API is available at `http://localhost:8000/api/`. Django admin is at `/admin/`.

For local development, install `requirements.txt` and run `python manage.py migrate` followed by `python manage.py runserver`. Local settings use SQLite unless `DB_ENGINE=postgres` is set. Set `DJANGO_DEBUG=1` for local debug pages if needed.

## API

- `POST /api/auth/register/` creates an account and its Free subscription. Body: `username`, `email`, `password`.
- `POST /api/auth/token/` returns JWT access and refresh tokens. Body: `username`, `password`.
- `POST /api/auth/token/refresh/` refreshes an access token.
- `GET, POST /api/projects/` lists or creates owned projects. Project responses include task counts and completion percentage.
- `GET, PATCH, DELETE /api/projects/{id}/` manage an owned project.
- `GET, POST /api/tasks/` lists or creates tasks for projects you own.
- `GET, PATCH, DELETE /api/tasks/{id}/` manage an owned task. Filter with `project`, `status`, or `priority`.
- `GET /api/billing/subscription/` returns the authenticated user's current plan and period.
- `GET /api/dashboard/summary/` returns the authenticated user's project totals and task totals, including open, overdue, and due-within-seven-days counts.

Send protected requests with `Authorization: Bearer <access-token>`. Project and task records are restricted to their owner. List endpoints are paginated; projects and tasks support search and ordering.

Subscription plans are currently data-model foundations only. No payment provider, plan changes, or billing webhooks are configured.

## Tests

```sh
python manage.py test
```