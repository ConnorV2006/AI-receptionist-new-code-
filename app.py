import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# -------------------------------------------------
# App Config
# -------------------------------------------------
app = Flask(__name__)

# Secret key
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# Login Manager
# -------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# -------------------------------------------------
# Import models
# -------------------------------------------------
from models import User, Role, Patient, Appointment, AuditLog, Clinic, DoctorNote, NurseProfile

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------------------------
# Routes
# -------------------------------------------------
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Split dashboard based on role"""
    if current_user.role and current_user.role.name == "superadmin":
        return render_template("dashboards/superadmin_dashboard.html", user=current_user)
    elif current_user.role and current_user.role.name == "doctor":
        return render_template("dashboards/doctor_dashboard.html", user=current_user)
    elif current_user.role and current_user.role.name == "nurse":
        return render_template("dashboards/nurse_dashboard.html", user=current_user)
    elif current_user.role and current_user.role.name == "receptionist":
        return render_template("dashboards/receptionist_dashboard.html", user=current_user)
    else:
        flash("No dashboard available for your role.", "warning")
        return redirect(url_for("logout"))


@app.route("/audit-logs")
@login_required
def audit_logs():
    """View system audit logs (restricted to superadmin)."""
    if not current_user.role or current_user.role.name != "superadmin":
        flash("Access denied: Superadmin only.", "danger")
        return redirect(url_for("dashboard"))

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()
    return render_template("audit_logs.html", logs=logs)

# -------------------------------------------------
# CLI command for manual seeding (optional)
# -------------------------------------------------
@app.cli.command("seed")
def seed_command():
    """Run the seeding script manually if needed."""
    from seed import run_seed
    run_seed()
    print("✅ Database seeded.")


# -------------------------------------------------
# App entry
# -------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
