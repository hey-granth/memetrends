# MemeTrends

MemeTrends is an API-only Django project that tracks trending memes
across Reddit and Twitter (X).\
It ingests memes directly from external APIs, calculates a trending
score based on engagement and time decay, and serves results via a clean
REST API.

------------------------------------------------------------------------

## Features

-   **Django REST Framework** backend (API-only).
-   **Authentication** with JWT (SimpleJWT).
-   **Async tasks** with Celery and Redis.
-   **Trending algorithm** using weighted engagement + time-decay.
-   **Redis leaderboard** for fast trending queries.
-   **External ingestion** from Reddit (via PRAW) and Twitter (via v2
    API).
-   **Dockerized** setup with Django, Postgres, Redis, Celery Worker,
    Celery Beat.

------------------------------------------------------------------------

## Tech Stack

-   Django 5.x + Django REST Framework
-   SQLite (default, can switch to Postgres)
-   Redis
-   Celery
-   Gunicorn
-   Docker + docker-compose

------------------------------------------------------------------------

## Getting Started

### 1. Clone the repo

``` bash
git clone https://github.com/hey-granth/memetrends.git
cd memetrends
```

### 2. Environment setup

Create a `.env` file in the project root:
    
    SECRET_KEY='your-django-secret-key'
    DEBUG=True
    CELERY_BROKER_URL="redis://localhost:6379/0"
    CELERY_RESULT_BACKEND="redis://localhost:6379/0"
    
    # Reddit API credentials
    REDDIT_CLIENT_ID='your-reddit-client-id'
    REDDIT_USER_AGENT='your-app-user-agent'
    REDDIT_CLIENT_SECRET='your-reddit-client-secret'
    
    # Twitter (X) API v2 credentials
    X_API_KEY='your-twitter-api-key'
    X_API_SECRET='your-twitter-api-secret'
    X_BEARER_TOKEN='your-twitter-bearer-token'

[//]: # (### 3. Build and run with Docker)

[//]: # ()
[//]: # (``` bash)

[//]: # (docker-compose build)

[//]: # (docker-compose up)

[//]: # (```)

API available at `http://localhost:8000/api/`

------------------------------------------------------------------------

## API Endpoints

-   `POST /api/token/` → Obtain JWT token
-   `POST /api/token/refresh/` → Refresh JWT
-   `GET /api/memes/` → List memes
-   `POST /api/memes/` → Add meme (auth required)
-   `GET /api/trending/` → Trending memes leaderboard

------------------------------------------------------------------------

## Tasks

Celery Beat schedules: - Fetch Reddit memes every 15 minutes - Fetch
Twitter memes every 30 minutes - Recompute trending scores every 5
minutes

------------------------------------------------------------------------

## Trending Score Formula

    engagement = (likes * 1) + (comments * 2) + (shares * 3)
    log_engagement = log10(max(engagement, 1))
    age_hours = max((now - posted_at).hours, 1)
    score = log_engagement / sqrt(age_hours)

------------------------------------------------------------------------

## Development

Run locally (without Docker):

``` bash
python manage.py runserver
celery -A memetrends worker -l info
celery -A memetrends beat -l info
```

------------------------------------------------------------------------

## Author
-   Granth Agarwal - [hey-granth](https://www.github.com/hey-granth)
