from flask import Flask, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import urllib.parse

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://username:password@mysql:3306/healthcare')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    return "Welcome to the Healthcare Portal"

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

@app.route('/doctors/register', methods=['POST'])
def register_doctor():
    data = request.get_json()
    new_doctor = Doctor(
        username=data['username'],
        password=data['password']  # Note: For production, store passwords securely using hashing
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({"message": "Doctor registered successfully"}), 201

@app.route('/doctors/login', methods=['POST'])
def login_doctor():
    data = request.get_json()
    doctor = Doctor.query.filter_by(username=data['username'], password=data['password']).first()
    if doctor:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

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
