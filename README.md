🛡️ ClientGuard - Telecom Churn Prediction System

ClientGuard is a comprehensive Full-Stack CRM and Analytics platform designed to predict customer churn in the telecommunications industry. Built with a microservices architecture using Docker, it combines a robust transactional database with a rule-based prediction engine to help managers retain at-risk customers.

🚀 Key Features

Hybrid Architecture: Functions as both a Web Application (GUI) and a RESTful API provider.

Churn Prediction Engine: A logic-based system that calculates risk scores (0-100%) based on tenure, contract type, and services.

Real-Time Analytics: Dashboard with dynamic Chart.js visualizations and live consultation logs via JS Polling.

Automated Reporting: Generates and downloads Executive PDF reports with financial summaries.

API Documentation: Fully documented endpoints using Swagger UI.

Dockerized: Zero-configuration deployment using Docker Compose.

📂 Project Structure

Here is an overview of the key files in this repository:

File / Folder

Description

app.py

The Core. Contains the Flask application, API routes, View controllers, and the Prediction Logic Engine.

models.py

Defines the Database Schema using SQLAlchemy ORM (Employee, Customer, Contract, etc.).

docker-compose.yml

Orchestrates the two services: web (Flask App) and db (MySQL Database).

Dockerfile

Instructions to build the Python environment image.

seed_raw.py

Utility Script. A standalone Python script using raw SQL to populate the database with 150+ dummy records (See usage below).

templates/

Contains the HTML files for the GUI (Jinja2 templates).

requirements.txt

List of Python dependencies.

🛠️ Installation & Setup

Prerequisites

Docker Desktop installed and running.

Git.

Step 1: Clone the Repository

git clone [https://github.com/YOUR_USERNAME/client-guard.git](https://github.com/YOUR_USERNAME/client-guard.git)
cd client-guard


Step 2: Build and Run

This command will download the images, build the app, and start the database.

docker-compose up --build


Wait until you see "Debugger is active" in the terminal.

🖥️ Usage

Accessing the Application

Open your browser and navigate to:

GUI Dashboard: http://localhost:5001

API Documentation (Swagger): http://localhost:5001/apidocs

Default Credentials

To log in as a Manager:

Username: admin

Password: admin123

🌱 Populating the Database (Optional)

The repository includes a utility script seed_raw.py to instantly fill the database with 150 realistic customers, contracts, and history logs using the Faker library.

Since the database runs inside a container, you must execute the script internally.

How to run it:

Ensure the app is running (docker-compose up).

Open a new terminal window.

Execute the following command to run the script inside the web container:

# If the file is already in the container (after a rebuild)
docker exec -it client-guard-web-1 python seed_raw.py


Note: If Docker complains that the file is not found (because you didn't rebuild), inject it first:

docker cp seed_raw.py client-guard-web-1:/app/seed_raw.py
docker exec -it client-guard-web-1 python seed_raw.py


(Replace client-guard-web-1 with your actual container name if different, check with docker ps).

📊 Logic Behind Prediction

The system does not use a "black box" model. Instead, it implements transparent business logic in app.py:

Tenure: Short tenure (< 6 months) increases risk.

Contract: "Month-to-month" contracts significantly increase risk.

Service: Fiber optic users have a slight risk adjustment due to market competition.

Demographics: Senior citizens have weighted retention factors.

If the calculated risk > 80%, the GUI automatically suggests retention strategies (e.g., "Offer 15% discount").

📝 License

This project is for educational purposes.
