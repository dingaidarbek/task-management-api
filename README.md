# Task Management API

A FastAPI-based task management application with JWT authentication, PostgreSQL database, and Docker support.

## Features

- User authentication with JWT tokens
- CRUD operations for tasks
- PostgreSQL database integration
- Docker and Docker Compose support
- CI/CD pipeline with GitHub Actions

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- PostgreSQL (if running locally)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd backend-hw1
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_management
SECRET_KEY=your-secret-key-keep-it-secret
```

## Running with Docker

1. Build and start the containers:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /token` - Get access token
- `POST /users/` - Create new user

### Tasks
- `GET /me` - Get current user info
- `POST /tasks/` - Create new task
- `GET /tasks/` - Get all tasks
- `GET /tasks/{task_id}` - Get specific task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

## Development

1. Run the application locally:
```bash
uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run tests with pytest:
```bash
pytest
```

## CI/CD

The project includes a GitHub Actions workflow that:
1. Runs tests on push and pull requests
2. Builds and pushes Docker image on main branch updates

## Security

- JWT authentication
- Password hashing with bcrypt
- Secure endpoints with user verification
- Environment variable configuration

## License

MIT 