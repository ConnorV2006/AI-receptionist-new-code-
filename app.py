import os
from flask import Flask, render_template, redirect, url_for, request, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
import csv
from io import StringIO, BytesIO

# PDF export
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# -------------------------------------------------
# App + Config
# -------------------------------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------------------------------------------------
# Login Manager
# -------------------------------------------------
login_manager = LoginManager(app)
login_manager.login_view = "login"

from models import User, AuditLog, Clinic, Patient, Visit, Paystub, Appointment, Reminder, FileUpload, CallLog, MessageLog, Role
from utils import is_superadmin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------------------------
# Auth Routes
# -------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# -------------------------------------------------
# Dashboard
# -------------------------------------------------
@app.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

# -------------------------------------------------
# Audit Logs Routes
# -------------------------------------------------
@app.route("/superadmin/audit-logs")
@login_required
def view_audit_logs():
    if not is_superadmin():
        abort(403)
    logs = filter_audit_logs()
    return render_template("audit_logs.html", logs=logs)


@app.route("/superadmin/audit-logs/export")
@login_required
def export_audit_logs():
    if not is_superadmin():
        abort(403)

    logs = filter_audit_logs()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["ID", "User", "Action", "Details", "Timestamp"])
    for log in logs:
        writer.writerow([
            log.id,
            log.user.email if log.user else "Unauthenticated",
            log.action,
            log.details or "-",
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        ])
    output = si.getvalue().encode("utf-8")
    si.close()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=audit_logs.csv"},
    )


@app.route("/superadmin/audit-logs/export/pdf")
@login_required
def export_audit_logs_pdf():
    if not is_superadmin():
        abort(403)

    logs = filter_audit_logs()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Audit Logs Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    data = [["ID", "User", "Action", "Details", "Timestamp"]]
    for log in logs:
        data.append([
            str(log.id),
            log.user.email if log.user else "Unauthenticated",
            log.action,
            log.details or "-",
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#333333")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return Response(
        buffer.getvalue(),
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=audit_logs.pdf"},
    )


@app.route("/superadmin/audit-logs/export/all")
@login_required
def export_all_audit_logs():
    if not is_superadmin():
        abort(403)

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["ID", "User", "Action", "Details", "Timestamp"])
    for log in logs:
        writer.writerow([
            log.id,
            log.user.email if log.user else "Unauthenticated",
            log.action,
            log.details or "-",
            log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        ])
    output = si.getvalue().encode("utf-8")
    si.close()

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=audit_logs_full.csv"},
    )


# -------------------------------------------------
# Shared Filtering Logic
# -------------------------------------------------
def filter_audit_logs():
    query = AuditLog.query

    user_email = request.args.get("user")
    if user_email:
        query = query.join(User).filter(User.email.ilike(f"%{user_email}%"))

    action = request.args.get("action")
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))

    start = request.args.get("start")
    end = request.args.get("end")

    if start:
        try:
            start_date = datetime.strptime(start, "%Y-%m-%d")
            query = query.filter(AuditLog.timestamp >= start_date)
        except ValueError:
            pass

    if end:
        try:
            end_date = datetime.strptime(end, "%Y-%m-%d")
            query = query.filter(AuditLog.timestamp <= end_date)
        except ValueError:
            pass

    return query.order_by(AuditLog.timestamp.desc()).all()


# -------------------------------------------------
# Run
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
