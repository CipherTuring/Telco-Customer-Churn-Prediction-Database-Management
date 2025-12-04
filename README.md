# ClientGuard - Telecom Churn Prediction System

ClientGuard is a comprehensive Full-Stack CRM and Analytics platform designed to predict customer churn in the telecommunications industry. Built with a microservices architecture using Docker, it combines a robust transactional database with a rule-based prediction engine to help managers retain at-risk customers.

## 🚀 Key Features

- **Hybrid Architecture:** Functions as a Web Application (GUI) via Server-Side Rendering and as a RESTful API provider.
- **Churn Prediction Engine:** Logic-based Python system calculating risk scores (0–100%) based on tenure, contract type, and services.
- **Real-Time Analytics:** Dashboard with Chart.js visualizations and live consultation logs using AJAX polling.
- **Automated Reporting:** Generates downloadable PDF reports using *FPDF*.
- **API Documentation:** Fully documented endpoints using Swagger UI (OpenAPI 2.0).
- **Dockerized Deployment:** Zero‑configuration setup with Docker Compose and persistent storage volumes.

## 📂 Project Structure

| File / Folder | Description |
|---------------|-------------|
| `app.py` | Core Flask application: API routes, controllers, prediction logic. |
| `models.py` | SQLAlchemy ORM models (Employee, Customer, Contract, etc.). |
| `docker-compose.yml` | Orchestrates the Flask web service and MySQL database. |
| `Dockerfile` | Builds the Python environment image. |
| `seed_raw.py` | Populates the database with 150+ dummy records. |
| `templates/` | Jinja2 HTML templates for GUI. |
| `requirements.txt` | Python dependencies list. |

## 🛠️ Installation & Setup

### Prerequisites
- Docker Desktop
- Git

### Step 1 — Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/client-guard.git
cd client-guard
```

### Step 2 — Build and Run
```bash
docker-compose up --build
```

Wait until you see **"Debugger is active"** in the terminal.

## 🔌 API Usage & Testing (cURL Examples)

Base URL: `http://localhost:5001/api`

### 1. GET — Retrieve All Customers
```bash
curl -X GET http://localhost:5001/api/customers
```

### 2. POST — Register a New Customer
```bash
curl -X POST http://localhost:5001/api/customers   -H "Content-Type: application/json"   -d '{
        "id": "API-TEST-001",
        "gender": "Female",
        "tenure": 12,
        "senior": false,
        "partner": true,
        "dependents": false
      }'
```

### 3. PUT — Update Customer Data
```bash
curl -X PUT http://localhost:5001/api/customers/API-TEST-001   -H "Content-Type: application/json"   -d '{"tenure": 24}'
```

### 4. DELETE — Remove a Customer
```bash
curl -X DELETE http://localhost:5001/api/customers/API-TEST-001
```

### 5. GET — Real-Time Logs
```bash
curl -X GET http://localhost:5001/api/recent_logs
```

## 🖥️ GUI Usage

- **Dashboard:** http://localhost:5001  
- **Swagger Docs:** http://localhost:5001/apidocs  

### Default Credentials
- **Username:** admin  
- **Password:** admin123  

## 🌱 Populating the Database (Optional)

Run the seed script inside the container:

```bash
docker exec -it client-guard-web-1 python seed_raw.py
```

If missing:
```bash
docker cp seed_raw.py client-guard-web-1:/app/seed_raw.py
docker exec -it client-guard-web-1 python seed_raw.py
```

## 📊 Logic Behind Prediction

- Tenure < 6 months → +20% risk  
- Month-to-month contract → +25% risk  
- Fiber optic service → +10% risk  
- Senior citizen → +5% risk  

If risk > 80%, GUI shows **Retention Strategy** suggestions (e.g., discounts).
