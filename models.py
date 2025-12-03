from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column('EmployeeID', db.String(10), primary_key=True)
    username = db.Column('Username', db.String(10), nullable=False)
    password = db.Column('Password', db.String(15), nullable=False)
    role = db.Column('Role', db.String(20), nullable=False)
    employee_name = db.Column('EmployeeName', db.String(20), nullable=False)

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column('CustomerID', db.String(10), primary_key=True)
    gender = db.Column('Gender', db.String(10), nullable=False)
    senior_citizen = db.Column('SeniorCitizen', db.Boolean, nullable=False)
    partner = db.Column('Partner', db.Boolean, nullable=False)
    dependents = db.Column('Dependents', db.Boolean, nullable=False)
    tenure = db.Column('Tenure', db.Integer, nullable=False)

    # Relaciones para facilitar el acceso a datos (opcional pero útil)
    contract = db.relationship('Contract', backref='customer', uselist=False)
    internet = db.relationship('InternetService', backref='customer', uselist=False)

class ConsultationLogs(db.Model):
    __tablename__ = 'consultation_logs'
    log_id = db.Column('LogID', db.String(50), primary_key=True)
    consultation_time = db.Column('ConsultationTime', db.String(50), nullable=False)
    employee_id = db.Column('EmployeeID', db.String(10), db.ForeignKey('employee.EmployeeID'))
    customer_id = db.Column('CustomerID', db.String(10), db.ForeignKey('customer.CustomerID'))

class Contract(db.Model):
    __tablename__ = 'contract'
    customer_id = db.Column('CustomerID', db.String(10), db.ForeignKey('customer.CustomerID'), primary_key=True)
    contract_mode = db.Column('ContractMode', db.String(15), nullable=False)
    paperless_billing = db.Column('PaperlessBilling', db.Boolean, nullable=False)
    payment_method = db.Column('PaymentMethod', db.String(50), nullable=False)
    monthly_charges = db.Column('MonthlyCharges', db.Float, nullable=False)
    total_charges = db.Column('TotalCharges', db.Float, nullable=False)

class InternetService(db.Model):
    __tablename__ = 'internet_service'
    customer_id = db.Column('CustomerID', db.String(10), db.ForeignKey('customer.CustomerID'), primary_key=True)
    internet_type = db.Column('InternetType', db.String(50), nullable=False)
    online_security = db.Column('OnlineSecurity', db.Boolean, nullable=False)
    online_backup = db.Column('OnlineBackup', db.Boolean, nullable=False)
    device_protection = db.Column('DeviceProtection', db.Boolean, nullable=False)
    tech_support = db.Column('TechSupport', db.Boolean, nullable=False)
    streaming_movies = db.Column('StreamingMovies', db.Boolean, nullable=False)

class PhoneService(db.Model):
    __tablename__ = 'phone_service'
    customer_id = db.Column('CustomerID', db.String(10), db.ForeignKey('customer.CustomerID'), primary_key=True)
    has_phone_service = db.Column('has_phone_service', db.Boolean, nullable=False)
    multiple_lines = db.Column('MultipleLines', db.Boolean, nullable=False)

class Predictions(db.Model):
    __tablename__ = 'predictions'
    customer_id = db.Column('CustomerID', db.String(10), db.ForeignKey('customer.CustomerID'), primary_key=True)
    churn_probability = db.Column('ChurnProbability', db.Float, nullable=False)