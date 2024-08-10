from flask import Flask, request, jsonify, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'mysql+pymysql://username:password@database-1.ct8686g6i2km.us-west-2.rds.amazonaws.com/healthcare'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    blood_group = db.Column(db.String(3), nullable=False)
    medical_record = db.Column(db.Text, nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = Doctor.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another one.", 400

        # Create a new doctor
        new_doctor = Doctor(username=username, password=password)
        db.session.add(new_doctor)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Authenticate the doctor
        doctor = Doctor.query.filter_by(username=username, password=password).first()
        if doctor:
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. Please try again.", 401
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the Doctor's Dashboard!"

@app.route('/patients', methods=['POST'])
def create_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        height=data['height'],
        weight=data['weight'],
        blood_group=data['blood_group'],
        medical_record=data['medical_record']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient created successfully"}), 201

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    patient = Patient.query.get_or_404(id)
    return jsonify({
        'name': patient.name,
        'age': patient.age,
        'gender': patient.gender,
        'height': patient.height,
        'weight': patient.weight,
        'blood_group': patient.blood_group,
        'medical_record': patient.medical_record
    })

@app.route('/routes')
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote(f"{rule.endpoint}: {methods} {url}")
        output.append(line)

    return "<br>".join(output)

# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
