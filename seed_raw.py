import pymysql
import random
import datetime
from faker import Faker

# Configuración
DB_HOST = 'db'
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_NAME = 'telco_db'

fake = Faker()

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def run_seed():
    print("🔌 Conectando directamente a MySQL...")
    connection = get_connection()
    
    try:
        with connection.cursor() as cursor:
            # 1. LIMPIEZA (Desactivando FKs temporalmente)
            print("🧹 Limpiando tablas...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            tables = ['consultation_logs', 'predictions', 'internet_service', 
                      'phone_service', 'contract', 'customer', 'employee']
            for table in tables:
                cursor.execute(f"TRUNCATE TABLE {table};")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            connection.commit()

            # 2. EMPLEADOS
            print("👤 Creando Empleados...")
            # Admin
            sql_emp = "INSERT INTO employee (EmployeeID, Username, Password, Role, EmployeeName) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_emp, ('EMP001', 'admin', 'admin123', 'Manager', 'Super Admin'))
            
            # Extras
            employees_ids = ['EMP001']
            for i in range(2, 6):
                eid = f'EMP{i:03d}'
                employees_ids.append(eid)
                cursor.execute(sql_emp, (
                    eid, fake.user_name(), 'password', 
                    random.choice(['Employee', 'Manager']), fake.name()
                ))
            connection.commit()

            # 3. CLIENTES Y SERVICIOS
            print("🚀 Generando 150 Clientes con datos completos...")
            
            # Preparamos las sentencias SQL
            sql_cust = "INSERT INTO customer (CustomerID, Gender, SeniorCitizen, Partner, Dependents, Tenure) VALUES (%s, %s, %s, %s, %s, %s)"
            sql_contract = "INSERT INTO contract (CustomerID, ContractMode, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges) VALUES (%s, %s, %s, %s, %s, %s)"
            sql_net = "INSERT INTO internet_service (CustomerID, InternetType, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingMovies) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            sql_phone = "INSERT INTO phone_service (CustomerID, has_phone_service, MultipleLines) VALUES (%s, %s, %s)"
            sql_pred = "INSERT INTO predictions (CustomerID, ChurnProbability) VALUES (%s, %s)"
            sql_log = "INSERT INTO consultation_logs (LogID, ConsultationTime, EmployeeID, CustomerID) VALUES (%s, %s, %s, %s)"

            customer_ids = []
            
            for i in range(150):
                cust_id = f"CUST-{i:04d}"
                customer_ids.append(cust_id)
                
                # Generar datos aleatorios
                gender = random.choice(['Male', 'Female'])
                tenure = random.randint(1, 72)
                
                # Ejecutar Insert Cliente
                cursor.execute(sql_cust, (
                    cust_id, gender, 
                    random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), 
                    tenure
                ))

                # Contrato
                monthly = round(random.uniform(20.0, 120.0), 2)
                cursor.execute(sql_contract, (
                    cust_id, 
                    random.choice(['Month-to-month', 'One year', 'Two year']),
                    random.choice([0, 1]),
                    random.choice(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card']),
                    monthly,
                    round(monthly * tenure, 2)
                ))

                # Internet
                inet_type = random.choice(['Fiber optic', 'DSL', 'No'])
                has_net = inet_type != 'No'
                cursor.execute(sql_net, (
                    cust_id, inet_type,
                    random.choice([0, 1]) if has_net else 0,
                    random.choice([0, 1]) if has_net else 0,
                    random.choice([0, 1]) if has_net else 0,
                    random.choice([0, 1]) if has_net else 0,
                    random.choice([0, 1]) if has_net else 0
                ))

                # Teléfono
                has_phone = random.choice([0, 1])
                cursor.execute(sql_phone, (
                    cust_id, has_phone,
                    random.choice([0, 1]) if has_phone else 0
                ))

                # Predicción
                cursor.execute(sql_pred, (
                    cust_id, round(random.random(), 2)
                ))

            connection.commit() # Guardamos el bloque grande

            # 4. LOGS
            print("📜 Generando Historial...")
            for cust_id in customer_ids:
                if random.random() > 0.6:
                    cursor.execute(sql_log, (
                        f"LOG-{fake.uuid4()[:8]}",
                        fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
                        random.choice(employees_ids),
                        cust_id
                    ))
            connection.commit()

            print("✨ ¡Éxito! Base de datos poblada al 100%.")

    except Exception as e:
        print(f"❌ Error fatal: {e}")
    finally:
        connection.close()

if __name__ == '__main__':
    run_seed()