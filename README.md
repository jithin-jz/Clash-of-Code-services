# Code of Clans - Backend Services

This directory contains the microservices that power the Code of Clans platform.

## Architecture

The backend is composed of three main services:

- **Core (`/core`)**: Django-based monolith handling Users, Authentication, Payments, and Gamification logic.
- **Chat (`/chat`)**: FastAPI + WebSocket service for real-time global chat.
- **AI (`/ai`)**: Python service for AI-powered features (content generation, moderation).

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1.  **Environment Setup**:
    Ensure you have a `.env` file in the `core` directory (and other services if required).
    
    *Example `core/.env`:*
    ```env
    SECRET_KEY=your_secret_key
    DEBUG=True
    DB_NAME=code_of_clan_db
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    # ... other integrations (GitHub, Google, Razorpay)
    ```

2.  **Run with Docker Compose**:
    Navigate to the `services/core` directory (where the main compose file resides) and run:

    ```bash
    cd core
    docker-compose up -d --build
    ```

    This will start:
    - `web`: The Django Core Service (Port 8000)
    - `chat`: The Chat Service (Port 8001)
    - `db`: PostgreSQL Database (Port 5433)
    - `redis`: Redis Cache/Message Broker (Port 6379)

3.  **Migrations**:
    If this is your first run, apply database migrations:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **Access**:
    - Backend API: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) (Swagger UI)
    - Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## Development

- **Logs**: `docker-compose logs -f`
- **Shell**: `docker-compose exec web bash`
