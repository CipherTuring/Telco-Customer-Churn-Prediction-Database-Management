# 🛡️ ClientGuard - Telecom Churn Prediction System

ClientGuard is a comprehensive Full-Stack CRM and Analytics platform designed to predict customer churn in the telecommunications industry. Built with a microservices architecture using Docker, it combines a robust transactional database with a rule-based prediction engine to help managers retain at-risk customers.

## 🚀 Key Features
- **Hybrid Architecture:** Functions as both a Web Application (GUI) and a RESTful API provider.
- **Churn Prediction Engine:** Calculates risk scores (0-100%) based on tenure, contract type, and services.
- **Real-Time Analytics:** Dashboard with dynamic Chart.js visualizations and live consultation logs via JS Polling.
- **Automated Reporting:** Generates Executive PDF reports with financial summaries.
- **API Documentation:** Swagger UI.
- **Dockerized:** Zero-configuration deployment using Docker Compose.

## 📂 Project Structure
| File / Folder | Description |
|--------------|-------------|
| **app.py** | Flask app, routes, logic engine |
| **models.py** | SQLAlchemy ORM models |
| **docker-compose.yml** | Orchestrates web + db services |
| **Dockerfile** | Python environment image |
| **seed_raw.py** | Populates DB with dummy data |
| **templates/** | Jinja2 HTML templates |
| **requirements.txt** | Dependencies |

## 🛠️ Installation & Setup
### Prerequisites
- Docker Desktop  
- Git

### Step 1: Clone the Repository
```
git clone https://github.com/YOUR_USERNAME/client-guard.git
cd client-guard
```

### Step 2: Build and Run
```
docker-compose up --build
```
Wait until **"Debugger is active"** appears.

## 🖥️ Usage
### Access the Application
- GUI: http://localhost:5001  
- Swagger Docs: http://localhost:5001/apidocs  

### Default Credentials
- Username: **admin**  
- Password: **admin123**

## 🌱 Populating the Database
```
docker exec -it client-guard-web-1 python seed_raw.py
```

If file missing:
```
docker cp seed_raw.py client-guard-web-1:/app/seed_raw.py
docker exec -it client-guard-web-1 python seed_raw.py
```

## 📊 Logic Behind Prediction
1. Short tenure → higher risk  
2. Month-to-month contract → higher risk  
3. Fiber optic → slight adjustment  
4. Senior citizens → weighted factors  

If **risk > 80%**, GUI suggests retention strategies (“Offer 15% discount”).

