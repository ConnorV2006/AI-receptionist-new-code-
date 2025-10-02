from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="staff")  # staff, admin, superadmin
    phone_number = db.Column(db.String(20))  # Added in migration 0002
    clinic_id = db.Column(db.Integer, db.ForeignKey("clinic.id"))  # Added in migration 0003

    audit_logs = db.relationship("AuditLog", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    slug = db.Column(db.String(50), unique=True)
    twilio_number = db.Column(db.String(20))
    twilio_sid = db.Column(db.String(120))
    twilio_token = db.Column(db.String(120))

    # Relationships
    users = db.relationship("User", backref="clinic", lazy=True)
    calls = db.relationship("CallLog", backref="clinic", lazy=True)
    messages = db.relationship("MessageLog", backref="clinic", lazy=True)


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


class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
