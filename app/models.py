from . import db
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(100), nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)


class Facilitator(db.Model):
    __tablename__ = 'facilitators'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crm_id = db.Column(db.String(50), nullable=False)  # external CRM reference
    events = db.relationship('Event', backref='facilitator', lazy=True)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150))

    latitude = db.Column(db.Float)   # New: to support proximity search
    longitude = db.Column(db.Float)  # New: to support proximity search

    type = db.Column(db.String(50))  # e.g., Yoga, Meditation
    status = db.Column(db.String(20), default='scheduled')  # scheduled, cancelled
    is_deleted = db.Column(db.Boolean, default=False)  # soft delete

    facilitator_id = db.Column(db.Integer, db.ForeignKey('facilitators.id'), nullable=False)
    bookings = db.relationship('Booking', backref='event', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Optional payment fields for future use
    is_paid = db.Column(db.Boolean, default=False)
    payment_id = db.Column(db.String(100))
    amount_paid = db.Column(db.Float)
