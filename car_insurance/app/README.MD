# Car Insurance API

## Setup

From the project root:

```powershell
cd car_insurance
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the requirements:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables

The application and Docker Compose configuration expect these variables:

```powershell
$env:POSTGRES_DB="car_insurance"
$env:POSTGRES_USER="postgres"
$env:POSTGRES_PASSWORD="postgres"
$env:POSTGRES_HOST="localhost"
$env:POSTGRES_PORT="5432"
```

## Run PostgreSQL With Docker

Start the PostgreSQL container:

```powershell
docker compose up -d
```

Stop the container:

```powershell
docker compose down
```

## Run the API

Start the FastAPI application with Uvicorn:

```powershell
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

