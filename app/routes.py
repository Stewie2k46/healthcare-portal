from flask import request, jsonify, url_for
from app import app, db
from app.models import Patient, Doctor
import urllib.parse

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
        password=data['password']  # Note: Store passwords securely using hashing in production
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
