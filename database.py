from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VenmoRequest(db.Model):
    __tablename__ = "venmo_requests"

    id = db.Column(db.String(50), primary_key=True) # same as the venmo request id
    username = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(300))
    created = db.Column(db.DateTime, nullable=False)
    paid = db.Column(db.Boolean, nullable=False)
    reminder_interval_minutes = db.Column(db.Integer, default=60, nullable=False)
    last_reminder_sent = db.Column(db.DateTime)
    reminder_count = db.Column(db.Integer, default=0)


class UserPhone(db.Model):
    __tablename__ = "user_phones"

    username = db.Column(db.String(100), primary_key=True)
    phone = db.Column(db.String(20))


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()