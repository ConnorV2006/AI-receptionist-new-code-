import os
from datetime import datetime
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import pandas as pd  # for Excel upload/export

# -------------------------------------------------
# App + Config
# -------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------
# Models
# -------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="staff")  # staff, admin, superadmin

class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    slug = db.Column(db.String(50), unique=True)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(120))
    twilio_token = db.Column(db.String(120))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    dob = db.Column(db.Date)
    visits = db.relationship("Visit", backref="patient", lazy=True)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    summary_pdf = db.Column(db.String(200))

class Paystub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee = db.Column(db.String(120))
    period = db.Column(db.String(50))
    gross = db.Column(db.Float)
    net = db.Column(db.Float)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(120))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    send_time = db.Column(db.DateTime)

class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    path = db.Column(db.String(300))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class CallLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))
    from_number = db.Column(db.String(20))
    to_number = db.Column(db.String(20))
    status = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class MessageLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))
    from_number = db.Column(db.String(20))
    to_number = db.Column(db.String(20))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------------------------------
# Auth Routes
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # TODO: hash in production
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid login")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------------------------------
# Dashboard
# -------------------------------------------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

# -------------------------------------------------
# Paystubs
# -------------------------------------------------
@app.route("/paystubs", methods=["GET", "POST"])
def paystubs():
    if request.method == "POST":
        file = request.files["paystubFile"]
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            if filename.endswith(".csv"):
                df = pd.read_csv(filepath)
            else:
                df = pd.read_excel(filepath)
            for _, row in df.iterrows():
                stub = Paystub(employee=row["Employee"], period=row["Period"], gross=row["Gross"], net=row["Net"])
                db.session.add(stub)
            db.session.commit()
            flash("Paystubs uploaded successfully")
            return redirect(url_for("paystubs"))
    stubs = Paystub.query.all()
    return render_template("paystubs.html", paystubs=stubs)

@app.route("/paystubs/export/<int:stub_id>")
def export_paystub(stub_id):
    stub = Paystub.query.get_or_404(stub_id)
    df = pd.DataFrame([{
        "Employee": stub.employee,
        "Period": stub.period,
        "Gross": stub.gross,
        "Net": stub.net
    }])
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"paystub_{stub.employee}.xlsx")

# -------------------------------------------------
# Appointments
# -------------------------------------------------
@app.route("/appointments", methods=["GET", "POST"])
def appointments():
    if request.method == "POST":
        name = request.form["patient_name"]
        date = request.form["date"]
        time = request.form["time"]
        appt = Appointment(patient_name=name, date=date, time=time)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for("appointments"))
    appts = Appointment.query.all()
    events = [{"title": a.patient_name, "start": f"{a.date}T{a.time}"} for a in appts]
    return render_template("appointments.html", appointments=events)

# -------------------------------------------------
# Reminders
# -------------------------------------------------
@app.route("/reminders", methods=["GET", "POST"])
def reminders():
    if request.method == "POST":
        phone = request.form["phone"]
        message = request.form["message"]
        send_time = request.form["send_time"]
        reminder = Reminder(phone=phone, message=message, send_time=send_time)
        db.session.add(reminder)
        db.session.commit()
        flash("Reminder scheduled")
        return redirect(url_for("reminders"))
    all_reminders = Reminder.query.all()
    return render_template("reminders.html", reminders=all_reminders)

# -------------------------------------------------
# Patient Visits
# -------------------------------------------------
@app.route("/patients/<int:patient_id>/visits")
def patient_visits(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template("visit_summary.html", patient=patient)

@app.route("/visits/export/<int:visit_id>")
def export_visit(visit_id):
    visit = Visit.query.get_or_404(visit_id)
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    output = BytesIO()
    doc = SimpleDocTemplate(output)
    styles = getSampleStyleSheet()
    story = [
        Paragraph(f"Visit Summary for Patient {visit.patient_id}", styles["Heading1"]),
        Paragraph(f"Date: {visit.date}", styles["Normal"]),
        Paragraph(f"Notes: {visit.notes}", styles["Normal"]),
    ]
    doc.build(story)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f"visit_{visit.id}.pdf")

# -------------------------------------------------
# Logs & Quick Replies
# -------------------------------------------------
@app.route("/audit-logs")
def audit_logs():
    calls = CallLog.query.all()
    msgs = MessageLog.query.all()
    logs = []
    for c in calls:
        logs.append({"type": "Call", "from_number": c.from_number, "to_number": c.to_number, "status": c.status, "timestamp": c.timestamp})
    for m in msgs:
        logs.append({"type": "Message", "from_number": m.from_number, "to_number": m.to_number, "body": m.body, "timestamp": m.timestamp})
    return render_template("audit_logs.html", logs=logs)

@app.route("/quick-replies", methods=["GET", "POST"])
def quick_replies():
    if "quick_replies" not in session:
        session["quick_replies"] = []
    if request.method == "POST":
        session["quick_replies"].append(request.form["reply"])
    return render_template("quick_replies.html", replies=session["quick_replies"])

@app.route("/quick-replies/delete/<int:idx>")
def delete_quick_reply(idx):
    if "quick_replies" in session and idx < len(session["quick_replies"]):
        session["quick_replies"].pop(idx)
    return redirect(url_for("quick_replies"))

# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
