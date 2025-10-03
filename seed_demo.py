from flask import current_app
from models import db
from sqlalchemy import text
from datetime import datetime, timedelta

def run_demo_seed():
    conn = db.session

    # same inserts from 0002_seed_demo_data.py go here
    # but wrapped with db.session.execute(...)
    # and finally db.session.commit()
