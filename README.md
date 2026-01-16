# Event Management API

## Description

REST API for managing events (conferences, meetups, workshops, etc.) built with Django and Django REST Framework.
Users can create events, register for them, view event lists, and manage their registrations.

## Technologies

* Python 3.11+
* Django 5.x
* Django REST Framework
* PostgreSQL
* django-filter (search and filtering)
* djangorestframework-simplejwt (JWT authentication)
* Docker (optional)

## Main Features

* CRUD operations for events (Event)
* User registration
* JWT token-based authentication
* Event registration / cancellation
* Event filtering, search, and ordering

## Installation and Running

### 1. Locally

1. Clone the repository:

```bash
git clone https://github.com/enCoder277/Event-API.git
cd Event-API
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Configure PostgreSQL and update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

6. Start the server:

```bash
python manage.py runserver
```

### 2. Docker

1. Install Docker and docker-compose
2. Start the project:

```bash
docker-compose up --build
```

3. The server will be available at `http://localhost:8000/`

---

## API Endpoints

### Authentication

* `POST /api/auth/register/` — register a user
* `POST /api/token/` — obtain JWT token
* `POST /api/token/refresh/` — refresh access token

### Events (Event)

* `GET /api/events/` — list events
* `GET /api/events/{id}/` — retrieve a single event
* `POST /api/events/` — create event (authenticated users only)
* `PUT /api/events/{id}/` — update event (organizer only)
* `DELETE /api/events/{id}/` — delete event (organizer only)

### Event Registration

* `POST /api/events/{id}/register/` — register for an event
* `DELETE /api/events/{id}/unregister/` — cancel registration
* `GET /api/events/my_registrations/` — list my registrations

### Filtering and Search

* Search by `title`, `description`, `location`, `organizer`: `?search=django`
* Filter by `location`: `?location=oslo`
* Filter by organizer: `?organizer=ruslan`
* Date range filter: `?date_from=2026-02-01T00:00:00Z&date_to=2026-02-28T23:59:59Z`
* Ordering: `?ordering=date` or `?ordering=-date`

---

## Example Requests (curl)

Obtain token:

```bash
curl -X POST http://localhost:8000/api/token/ -H "Content-Type: application/json" -d '{"username":"ruslan","password":"password123"}'
```

Create an event (with Authorization header):

```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"title":"Django Meetup","description":"Learn DRF with JWT","date":"2026-02-01T18:00:00Z","location":"Oslo"}'
```

Register for an event:

```bash
curl -X POST http://localhost:8000/api/events/1/register/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
