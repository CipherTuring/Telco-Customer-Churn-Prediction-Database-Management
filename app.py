import os
import time
import datetime
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash, Response
from sqlalchemy import func
from models import db, Customer, Employee, Predictions, ConsultationLogs, InternetService, Contract, PhoneService
from fpdf import FPDF
from flasgger import Swagger 

app = Flask(__name__)

# --- CONFIGURATION ---
app.secret_key = 'clientguard_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Swagger Config
app.config['SWAGGER'] = {
    'title': 'ClientGuard API',
    'uiversion': 3
}

swagger = Swagger(app)
db.init_app(app)

def wait_for_db():
    with app.app_context():
        print("Connecting to DB...")
        time.sleep(10)
        try:
            db.create_all()
            print("DB Connected successfully!")
        except Exception as e:
            print(f"DB Error: {e}")


#  LOGIC ENGINE (BUSINESS LOGIC)
def calculate_churn_risk(customer, contract, internet):
    """
    Calculates risk based on REAL database attributes.
    """
    score = 0.30 # Base risk

    # 1. Tenure
    if customer.tenure < 6: score += 0.20
    elif customer.tenure > 24: score -= 0.15

    # 2. Contract (High impact)
    if contract:
        if contract.contract_mode == 'Month-to-month': score += 0.25
        elif contract.contract_mode == 'Two year': score -= 0.20

    # 3. Internet
    if internet and internet.internet_type == 'Fiber optic': score += 0.10

    # 4. Demographics
    if customer.senior_citizen: score += 0.05
    if not customer.partner and not customer.dependents: score += 0.05 # Alone = higher risk

    return max(0.01, min(0.99, score))

def get_retention_strategies(customer, contract, risk_score):
    strategies = []
    
    if risk_score > 0.80:
        if contract and contract.contract_mode == 'Month-to-month':
            strategies.append({
                "title": "Contract Stabilization",
                "desc": "User is on a volatile Month-to-month plan. Offer 20% off for 6 months to switch to a 1-Year contract."
            })
        
        if customer.tenure > 24:
            strategies.append({
                "title": "VIP Retention",
                "desc": "Long-term high-risk customer. Authorize a 'Loyalty Speed Boost' or free equipment upgrade."
            })
        else:
            strategies.append({
                "title": "Onboarding Rescue",
                "desc": "New customer at risk. Schedule a call with a Success Manager immediately."
            })
            
    return strategies

<<<<<<< HEAD
# ==========================================
#  ZONA API RESTful
# ==========================================
=======
>>>>>>> ea8cb0ce8b092116bb2c0de5d42614f6abc76497

#  API RESTful
@app.route('/api/customers', methods=['GET'])
def api_get_customers():
    """
    Obtener todos los clientes
    ---
    tags:
      - Customers
    responses:
      200:
        description: Lista de clientes activos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "CUST-001"
              gender:
                type: string
              tenure:
                type: integer
    """
    customers = Customer.query.all()
    output = []
    for c in customers:
        output.append({'id': c.customer_id, 'gender': c.gender, 'tenure': c.tenure})
    return jsonify(output)

@app.route('/api/customers', methods=['POST'])
def api_create_customer():
    """
    Crear un nuevo cliente
    ---
    tags:
      - Customers
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - id
          properties:
            id:
              type: string
              example: "CUST-999"
            gender:
              type: string
              example: "Female"
            tenure:
              type: integer
              example: 5
    responses:
      201:
        description: Cliente creado exitosamente
      500:
        description: Error al crear
    """
    data = request.json
    try:
        new_cust = Customer(
            customer_id=data['id'],
            gender=data.get('gender', 'Male'),
            senior_citizen=data.get('senior', False),
            partner=data.get('partner', False),
            dependents=data.get('dependents', False),
            tenure=data.get('tenure', 0)
        )
        db.session.add(new_cust)
        db.session.commit()
        return jsonify({'message': 'Cliente creado', 'id': new_cust.customer_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<id>', methods=['PUT'])
def api_update_customer(id):
    """
    Actualizar datos de un cliente
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
        type: string
        required: true
        description: ID del cliente a actualizar
      - in: body
        name: body
        schema:
          type: object
          properties:
            tenure:
              type: integer
              description: Nueva antigüedad
              example: 24
    responses:
      200:
        description: Cliente actualizado
      404:
        description: Cliente no encontrado
    """
    data = request.json
    customer = Customer.query.get(id)
    if not customer: return jsonify({'message': 'Cliente no encontrado'}), 404
    
    if 'tenure' in data: customer.tenure = data['tenure']
    db.session.commit()
    return jsonify({'message': f'Cliente {id} actualizado'})

@app.route('/api/customers/<id>', methods=['DELETE'])
def api_delete_customer(id):
    """
    Eliminar un cliente
    ---
    tags:
      - Customers
    parameters:
      - in: path
        name: id
        type: string
        required: true
        description: ID del cliente a eliminar
    responses:
      200:
        description: Cliente eliminado
      404:
        description: Cliente no encontrado
    """
    customer = Customer.query.get(id)
    if not customer: return jsonify({'message': 'Cliente no encontrado'}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': f'Cliente {id} eliminado'})

@app.route('/api/recent_logs', methods=['GET'])
def api_recent_logs():
    """
    Ver logs en tiempo real (Monitor)
    ---
    tags:
      - Monitoring
    responses:
      200:
        description: Últimos 10 eventos del sistema
    """
    logs = db.session.query(ConsultationLogs, Employee, Customer).\
        join(Employee, ConsultationLogs.employee_id == Employee.employee_id).\
        join(Customer, ConsultationLogs.customer_id == Customer.customer_id).\
        order_by(ConsultationLogs.consultation_time.desc()).limit(10).all()
    
    data = []
    for log, emp, cust in logs:
        data.append({
            'time': log.consultation_time,
            'employee': emp.employee_name,
            'role': emp.role,
            'customer': cust.customer_id
        })
    return jsonify(data)


#  GUI ROUTES
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Employee.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.employee_id
            session['user_name'] = user.employee_name
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    results = db.session.query(Customer, Predictions).outerjoin(Predictions, Customer.customer_id == Predictions.customer_id).all()
    
    # Simple analytics for charts
    internet_stats = db.session.query(InternetService.internet_type, func.count(InternetService.customer_id)).group_by(InternetService.internet_type).all()
    labels_int = [x[0] for x in internet_stats]
    data_int = [x[1] for x in internet_stats]

    contract_stats = db.session.query(Contract.contract_mode, func.count(Contract.customer_id)).group_by(Contract.contract_mode).all()
    labels_cont = [x[0] for x in contract_stats]
    data_cont = [x[1] for x in contract_stats]

    payment_stats = db.session.query(Contract.payment_method, func.count(Contract.customer_id)).group_by(Contract.payment_method).all()
    labels_pay = [x[0] for x in payment_stats]
    data_pay = [x[1] for x in payment_stats]
    
    return render_template('dashboard.html', 
                           data=results, 
                           labels_int=labels_int, data_int=data_int,
                           labels_cont=labels_cont, data_cont=data_cont,
                           labels_pay=labels_pay, data_pay=data_pay,
                           user=session['user_name'])

# PREDICTION TOOL
@app.route('/predict', methods=['GET', 'POST'])
def predict_tool():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    result = None
    strategies = []
    customer_data = None
    
    if request.method == 'POST':
        cust_id = request.form['customer_id']
        
        
        customer = Customer.query.get(cust_id)
        
        if customer:
            
            pred = Predictions.query.get(cust_id)
            
            if pred:
                
                risk_score = pred.churn_probability
                flash(f'Análisis recuperado de la base de datos para {cust_id}.', 'info')
            else:
                
                contract = Contract.query.get(cust_id)
                internet = InternetService.query.get(cust_id)
                
                risk_score = calculate_churn_risk(customer, contract, internet)
                
                n
                pred = Predictions(customer_id=cust_id, churn_probability=risk_score)
                db.session.add(pred)
                flash(f'Nuevo análisis generado y guardado para {cust_id}.', 'success')
            
            
            try:
                new_log = ConsultationLogs(
                    log_id=f"LOG-{int(time.time())}",
                    consultation_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    employee_id=session['user_id'],
                    customer_id=cust_id
                )
                db.session.add(new_log)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(f"Error logging: {e}")
            
            
            result = {
                'score': round(risk_score * 100, 1),
                'risk_level': 'High' if risk_score > 0.5 else 'Low'
            }
            
            
            if risk_score > 0.80:
                # Recuperamos los objetos si no los tenemos cargados del "Caso B"
                contract = Contract.query.get(cust_id)
                strategies = get_retention_strategies(customer, contract, risk_score)
                
            customer_data = customer 
            
        else:
            flash(f'Customer {cust_id} not found.', 'danger')

    return render_template('predict.html', result=result, strategies=strategies, c=customer_data)
<<<<<<< HEAD

# --- CRUD OPERATIONS ---
=======
>>>>>>> ea8cb0ce8b092116bb2c0de5d42614f6abc76497

# CRUD OPERATIONS
@app.route('/add_web', methods=['POST'])
def add_customer_web():
    if 'user_id' not in session: return redirect(url_for('login'))
    try:
        # 1. Create Customer with ALL attributes
        new_cust = Customer(
            customer_id=request.form['id'],
            gender=request.form['gender'],
            senior_citizen='senior' in request.form,
            partner='partner' in request.form,        # New
            dependents='dependents' in request.form,  # New
            tenure=int(request.form['tenure'])
        )
        db.session.add(new_cust)

        
        new_contract = Contract(customer_id=new_cust.customer_id, contract_mode="Month-to-month", paperless_billing=0, payment_method="Mailed check", monthly_charges=0, total_charges=0)
        db.session.add(new_contract)
        
        new_internet = InternetService(customer_id=new_cust.customer_id, internet_type="No", online_security=0, online_backup=0, device_protection=0, tech_support=0, streaming_movies=0)
        db.session.add(new_internet)

        new_phone = PhoneService(customer_id=new_cust.customer_id, has_phone_service=0, multiple_lines=0)
        db.session.add(new_phone)
        
        
        
        db.session.commit()
        flash('Customer registered. Status: Pending Analysis (N/A).', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/update_web', methods=['POST'])
def update_customer_web():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    cust_id = request.form['id']
    customer = Customer.query.get(cust_id)
    
    if customer:
        customer.gender = request.form['gender']
        customer.tenure = int(request.form['tenure'])
        customer.senior_citizen = 'senior' in request.form
        # New fields
        customer.partner = 'partner' in request.form
        customer.dependents = 'dependents' in request.form
            
        db.session.commit()
        flash(f'Customer {cust_id} attributes updated.', 'info')
    
    return redirect(url_for('dashboard'))

@app.route('/delete_web/<id>')
def delete_customer_web(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    Predictions.query.filter_by(customer_id=id).delete()
    InternetService.query.filter_by(customer_id=id).delete()
    Contract.query.filter_by(customer_id=id).delete()
    PhoneService.query.filter_by(customer_id=id).delete()
    ConsultationLogs.query.filter_by(customer_id=id).delete()
    
    customer = Customer.query.get(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        flash(f'Customer {id} deleted.', 'warning')
    return redirect(url_for('dashboard'))

@app.route('/employees', methods=['GET', 'POST'])
def employees():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            new_emp = Employee(
                employee_id=request.form['id'],
                username=request.form['username'],
                password=request.form['password'],
                role=request.form['role'],
                employee_name=request.form['name']
            )
            db.session.add(new_emp)
            db.session.commit()
            flash('Employee registered successfully.', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('employees'))

    all_employees = Employee.query.all()
    return render_template('employees.html', employees=all_employees)

@app.route('/delete_employee/<id>')
def delete_employee(id):
    if 'user_id' not in session: return redirect(url_for('login'))
    if id == session['user_id']:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('employees'))
    emp = Employee.query.get(id)
    if emp:
        db.session.delete(emp)
        db.session.commit()
        flash('Employee deleted.', 'warning')
    return redirect(url_for('employees'))

@app.route('/services/<customer_id>', methods=['GET', 'POST'])
def manage_services(customer_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
   
    customer = Customer.query.get_or_404(customer_id)
    contract = Contract.query.get(customer_id)
    internet = InternetService.query.get(customer_id)
    phone = PhoneService.query.get(customer_id)

    if request.method == 'POST':
        
        if not contract:
            contract = Contract(customer_id=customer_id, contract_mode="Month-to-month", paperless_billing=0, payment_method="Mailed check", monthly_charges=0, total_charges=0)
            db.session.add(contract)
        
        contract.contract_mode = request.form['contract_mode']
        contract.paperless_billing = 'paperless' in request.form
        contract.payment_method = request.form['payment_method']
        
        contract.monthly_charges = float(request.form['monthly']) if request.form['monthly'] else 0.0
        contract.total_charges = float(request.form['total']) if request.form['total'] else 0.0

        
        if not internet:
            internet = InternetService(customer_id=customer_id, internet_type="No", online_security=0, online_backup=0, device_protection=0, tech_support=0, streaming_movies=0)
            db.session.add(internet)
            
        internet.internet_type = request.form['internet_type']
        internet.online_security = 'security' in request.form
        internet.online_backup = 'backup' in request.form
        internet.device_protection = 'protection' in request.form
        internet.tech_support = 'support' in request.form
        internet.streaming_movies = 'streaming' in request.form

    
        if not phone:
            phone = PhoneService(customer_id=customer_id, has_phone_service=0, multiple_lines=0)
            db.session.add(phone)
            
        phone.has_phone_service = 'phone' in request.form
        phone.multiple_lines = 'lines' in request.form

        
        # Calculate Churn
        
        new_risk = calculate_churn_risk(customer, contract, internet)
        
        # Save in predictions
        pred = Predictions.query.get(customer_id)
        if not pred:
            pred = Predictions(customer_id=customer_id)
            db.session.add(pred)
        pred.churn_probability = new_risk

        db.session.commit()
        
        flash('Services updated and Churn Probability recalculated.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('services.html', c=customer, k=contract, i=internet, p=phone)

@app.route('/history')
def history():
    return render_template('history.html')


#  REPORTING MODULE

class PDF(FPDF):
    def header(self):
        
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ClientGuard - Executive Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

@app.route('/reports')
def reports():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    total_customers = Customer.query.count()
    
    total_revenue = db.session.query(func.sum(Contract.monthly_charges)).scalar() or 0
    
    avg_churn = db.session.query(func.avg(Predictions.churn_probability)).scalar() or 0
    
    high_risk_count = Predictions.query.filter(Predictions.churn_probability > 0.80).count()
    
    contracts = db.session.query(Contract.contract_mode, func.count(Contract.customer_id)).group_by(Contract.contract_mode).all()

    return render_template('reports.html', 
                           total=total_customers, 
                           revenue=round(total_revenue, 2),
                           avg_churn=round(avg_churn * 100, 1),
                           risk_count=high_risk_count,
                           contracts=contracts)

@app.route('/download_report')
def download_report():
    if 'user_id' not in session: return redirect(url_for('login'))
    
    total_revenue = db.session.query(func.sum(Contract.monthly_charges)).scalar() or 0
    high_risk_customers = db.session.query(Customer, Predictions).join(Predictions).filter(Predictions.churn_probability > 0.80).limit(20).all()
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="1. Executive Summary", ln=True)
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(200, 10, txt=f"Total Monthly Revenue: ${round(total_revenue, 2):,}", ln=True)
    pdf.cell(200, 10, txt=f"High Risk Customers (>80%): {len(high_risk_customers)} (Showing top 20)", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="2. Priority Action List (High Risk)", ln=True)
    pdf.set_font("Arial", size=10)
    
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(40, 10, 'Customer ID', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Tenure', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Contract', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Risk %', 1, 1, 'C', 1)
    
    for cust, pred in high_risk_customers:
        contract = Contract.query.get(cust.customer_id)
        mode = contract.contract_mode if contract else "N/A"
        
        pdf.cell(40, 10, str(cust.customer_id), 1)
        pdf.cell(30, 10, f"{cust.tenure} months", 1)
        pdf.cell(40, 10, str(mode), 1)
        
        pdf.set_text_color(220, 50, 50)
        pdf.cell(30, 10, f"{int(pred.churn_probability * 100)}%", 1, 1, 'C')
        pdf.set_text_color(0, 0, 0) # Reset color

    response = pdf.output(dest='S').encode('latin-1')
    
    from flask import Response
    return Response(response, mimetype='application/pdf', headers={
        'Content-Disposition': 'attachment;filename=clientguard_report.pdf'
    })


if __name__ == '__main__':
    wait_for_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
