import os
from flask import Flask, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# -------------------------------------------------
# App + Config
# -------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models
from models import (
    User, Role, Patient, Appointment, DoctorNote,
    NurseProfile, ReceptionistProfile, AuditLog, TwilioLog
)

# -------------------------------------------------
# Home Route
# -------------------------------------------------
@app.route("/")
def home():
    return render_template_string("""
    <h1>AI Receptionist Demo</h1>
    <ul>
        <li><a href="/patients">Patients</a></li>
        <li><a href="/appointments">Appointments</a></li>
        <li><a href="/notes">Doctor Notes</a></li>
        <li><a href="/nurse_profiles">Nurse Profiles</a></li>
        <li><a href="/receptionist_profiles">Receptionist Profiles</a></li>
        <li><a href="/audit_logs">Audit Logs</a></li>
        <li><a href="/twilio_logs">Twilio Logs (SMS, Calls, Fax)</a></li>
    </ul>
    """)

# -------------------------------------------------
# Patients
# -------------------------------------------------
@app.route("/patients")
def list_patients():
    patients = Patient.query.all()
    return jsonify([{
        "id": p.id,
        "first_name": p.first_name,
        "last_name": p.last_name,
        "email": p.email,
        "phone": p.phone
    } for p in patients])

# -------------------------------------------------
# Appointments
# -------------------------------------------------
@app.route("/appointments")
def list_appointments():
    appts = Appointment.query.order_by(Appointment.scheduled_time).all()
    return jsonify([{
        "id": a.id,
        "patient_id": a.patient_id,
        "doctor_id": a.doctor_id,
        "scheduled_time": a.scheduled_time.isoformat()
    } for a in appts])

# -------------------------------------------------
# Doctor Notes
# -------------------------------------------------
@app.route("/notes")
def list_notes():
    notes = DoctorNote.query.all()
    return jsonify([{
        "id": n.id,
        "doctor_id": n.doctor_id,
        "patient_id": n.patient_id,
        "content": n.content,
        "created_at": n.created_at.isoformat() if n.created_at else None
    } for n in notes])

# -------------------------------------------------
# Nurse Profiles
# -------------------------------------------------
@app.route("/nurse_profiles")
def list_nurse_profiles():
    nurses = NurseProfile.query.all()
    return jsonify([{
        "id": n.id,
        "nurse_id": n.nurse_id,
        "department": n.department
    } for n in nurses])

# -------------------------------------------------
# Receptionist Profiles
# -------------------------------------------------
@app.route("/receptionist_profiles")
def list_receptionist_profiles():
    recs = ReceptionistProfile.query.all()
    return jsonify([{
        "id": r.id,
        "receptionist_id": r.receptionist_id,
        "front_desk": r.front_desk
    } for r in recs])

# -------------------------------------------------
# Audit Logs
# -------------------------------------------------
@app.route("/audit_logs")
def list_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return jsonify([{
        "id": l.id,
        "user_id": l.user_id,
        "action": l.action,
        "details": l.details,
        "timestamp": l.timestamp.isoformat() if l.timestamp else None
    } for l in logs])

# -------------------------------------------------
# Twilio Logs (SMS, Calls, Faxes)
# -------------------------------------------------
@app.route("/twilio_logs")
def list_twilio_logs():
    logs = TwilioLog.query.order_by(TwilioLog.timestamp.desc()).all()
    return jsonify([{
        "id": t.id,
        "type": t.type,
        "from_number": t.from_number,
        "to_number": t.to_number,
        "content": t.content,
        "status": t.status,
        "timestamp": t.timestamp.isoformat() if t.timestamp else None
    } for t in logs])

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
