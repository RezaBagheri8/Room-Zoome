# Roome Zoome Back-End

A FastAPI application with PostgreSQL database integration, using SQLAlchemy ORM and Alembic for migrations.

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

Create a `.env` file in the project root with the following content:

```
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=resume-builder
POSTGRES_PORT=5432
```

5. Create the database:

Create a PostgreSQL database named `resume-builder` using a tool like pgAdmin, DBeaver, or Navicat.

6. Run database migrations:

```bash
alembic upgrade head
```

## Running the Application

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload
```

The API will be available at:
- http://127.0.0.1:8000

## API Documentation

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Project Structure

```
├── alembic/              # Database migration files
│   ├── versions/         # Migration version files
│   └── env.py            # Alembic environment configuration
├── app/                  # Application code
│   ├── api/              # API endpoints
│   │   ├── endpoints/    # API route handlers
│   │   └── router.py     # Main API router
│   ├── core/             # Core application code
│   │   └── config.py     # Application configuration
│   ├── db/               # Database related code
│   │   └── session.py    # Database session
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic
│   └── repositories/     # Data access layer
├── .env                  # Environment variables
├── alembic.ini           # Alembic configuration
├── main.py               # Application entry point
└── requirements.txt      # Project dependencies
```

## Development

### Creating New Migrations

After making changes to your SQLAlchemy models:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## API Endpoints

### Resume Endpoints
- **PUT /resume/personal-info**: Update or create personal information for the current user.
- **GET /resume/personal-info**: Retrieve personal information for the current user.
- **PUT /resume/contact-info**: Update or create contact information for the current user.
- **GET /resume/contact-info**: Retrieve contact information for the current user.
- **POST /resume/social-media**: Add a new social media profile for the current user.

### User Endpoints
- **PATCH /users/profile**: Update the user's profile information, including optional profile picture upload.

### Auth Endpoints
- **POST /request-otp**: Request an OTP for phone number verification.
- **POST /verify-otp**: Verify the OTP and authenticate the user.
