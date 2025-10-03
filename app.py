import os
from flask import Flask, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
# Base HTML Dashboard Layout
# -------------------------------------------------
BASE_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
  <title>AI Receptionist Demo</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #f7f9fc; }
    header { background: #8B0000; color: white; padding: 15px; font-size: 22px; }
    .container { display: flex; }
    nav { width: 220px; background: #333; min-height: 100vh; color: white; padding: 20px 0; }
    nav h3 { margin-left: 20px; font-size: 16px; color: #ccc; text-transform: uppercase; }
    nav a { display: block; color: white; padding: 12px 20px; text-decoration: none; }
    nav a:hover { background: #444; }
    main { flex: 1; padding: 20px; }
    h1 { margin-top: 0; color: #333; }
    table { border-collapse: collapse; width: 100%; margin-top: 15px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    th { background: #f2f2f2; }
    tr:hover { background: #f9f9f9; }
  </style>
</head>
<body>
  <header>AI Receptionist Dashboard</header>
  <div class="container">
    <nav>
      <h3>Navigation</h3>
      <a href="/">🏠 Home</a>
      <a href="/patients">👩‍⚕️ Patients</a>
      <a href="/appointments">📅 Appointments</a>
      <a href="/notes">📝 Doctor Notes</a>
      <a href="/nurse_profiles">👩‍⚕️ Nurses</a>
      <a href="/receptionist_profiles">👩 Receptionists</a>
      <a href="/audit_logs">📊 Audit Logs</a>
      <a href="/twilio_logs">📞 Twilio Logs</a>
    </nav>
    <main>
      <h1>{{ title }}</h1>
      {{ body|safe }}
    </main>
  </div>
</body>
</html>
"""

# -------------------------------------------------
# Home Route
# -------------------------------------------------
@app.route("/")
def home():
    body = """
    <p>Welcome to the <b>AI Receptionist Demo</b> dashboard.</p>
    <p>Use the navigation menu on the left to explore demo data for patients, appointments, doctor notes, staff profiles, logs, and Twilio activity.</p>
    """
    return render_template_string(BASE_DASHBOARD, title="Home", body=body)

# -------------------------------------------------
# Patients
# -------------------------------------------------
@app.route("/patients")
def list_patients():
    patients = Patient.query.all()
    body = "<table><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th></tr>"
    for p in patients:
        body += f"<tr><td>{p.id}</td><td>{p.first_name} {p.last_name}</td><td>{p.email}</td><td>{p.phone}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Patients", body=body)

# -------------------------------------------------
# Appointments
# -------------------------------------------------
@app.route("/appointments")
def list_appointments():
    appts = Appointment.query.order_by(Appointment.scheduled_time).all()
    body = "<table><tr><th>ID</th><th>Patient</th><th>Doctor</th><th>Time</th></tr>"
    for a in appts:
        body += f"<tr><td>{a.id}</td><td>{a.patient_id}</td><td>{a.doctor_id}</td><td>{a.scheduled_time}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Appointments", body=body)

# -------------------------------------------------
# Doctor Notes
# -------------------------------------------------
@app.route("/notes")
def list_notes():
    notes = DoctorNote.query.all()
    body = "<table><tr><th>ID</th><th>Doctor</th><th>Patient</th><th>Note</th><th>Created</th></tr>"
    for n in notes:
        body += f"<tr><td>{n.id}</td><td>{n.doctor_id}</td><td>{n.patient_id}</td><td>{n.content}</td><td>{n.created_at}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Doctor Notes", body=body)

# -------------------------------------------------
# Nurse Profiles
# -------------------------------------------------
@app.route("/nurse_profiles")
def list_nurse_profiles():
    nurses = NurseProfile.query.all()
    body = "<table><tr><th>ID</th><th>User</th><th>Department</th></tr>"
    for n in nurses:
        body += f"<tr><td>{n.id}</td><td>{n.nurse_id}</td><td>{n.department}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Nurse Profiles", body=body)

# -------------------------------------------------
# Receptionist Profiles
# -------------------------------------------------
@app.route("/receptionist_profiles")
def list_receptionist_profiles():
    recs = ReceptionistProfile.query.all()
    body = "<table><tr><th>ID</th><th>User</th><th>Front Desk</th></tr>"
    for r in recs:
        body += f"<tr><td>{r.id}</td><td>{r.receptionist_id}</td><td>{r.front_desk}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Receptionist Profiles", body=body)

# -------------------------------------------------
# Audit Logs
# -------------------------------------------------
@app.route("/audit_logs")
def list_audit_logs():
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    body = "<table><tr><th>ID</th><th>User</th><th>Action</th><th>Details</th><th>Timestamp</th></tr>"
    for l in logs:
        body += f"<tr><td>{l.id}</td><td>{l.user_id}</td><td>{l.action}</td><td>{l.details}</td><td>{l.timestamp}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Audit Logs", body=body)

# -------------------------------------------------
# Twilio Logs (SMS, Calls, Faxes)
# -------------------------------------------------
@app.route("/twilio_logs")
def list_twilio_logs():
    logs = TwilioLog.query.order_by(TwilioLog.timestamp.desc()).all()
    body = "<table><tr><th>ID</th><th>Type</th><th>From</th><th>To</th><th>Content</th><th>Status</th><th>Time</th></tr>"
    for t in logs:
        body += f"<tr><td>{t.id}</td><td>{t.type}</td><td>{t.from_number}</td><td>{t.to_number}</td><td>{t.content}</td><td>{t.status}</td><td>{t.timestamp}</td></tr>"
    body += "</table>"
    return render_template_string(BASE_DASHBOARD, title="Twilio Logs", body=body)

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
