from flask import Blueprint, request, jsonify
from . import db
from .models import User, Event, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from datetime import datetime
from .crm import notify_crm

bp = Blueprint('main', __name__)

# -------- AUTH --------

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'msg': 'Email already registered'}), 400
    
    hashed_pw = generate_password_hash(data['password'])
    new_user = User(email=data['email'], name=data['name'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'Registration successful'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify({'access_token': access_token}), 200


# -------- EVENTS --------

@bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Event.query.all()
    output = []
    for e in events:
        output.append({
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'date': e.date.isoformat(),
            'location': e.location,
            'facilitator_id': e.facilitator_id
        })
    return jsonify({'events': output})


# -------- BOOKING --------

@bp.route('/book', methods=['POST'])
@jwt_required()
def book_event():
    data = request.get_json()
    user_id = get_jwt_identity()
    event = Event.query.get(data['event_id'])

    if not event:
        return jsonify({'msg': 'Event not found'}), 404

    new_booking = Booking(user_id=user_id, event_id=event.id)
    db.session.add(new_booking)
    db.session.commit()

    notify_crm(booking=new_booking)  # call CRM webhook function

    return jsonify({'msg': 'Booking successful'}), 201


@bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    user_id = int(get_jwt_identity())
    now = datetime.utcnow()
    
    past = []
    upcoming = []

    bookings = Booking.query.filter_by(user_id=user_id).all()

    for b in bookings:
        event = b.event
        facilitator = event.facilitator
        event_data = {
            "booked_at": b.booked_at.isoformat(),
            "event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location,
                "facilitator": facilitator.name
            }
        }

        if event.date < now:
            past.append(event_data)
        else:
            upcoming.append(event_data)

    return jsonify({
        "past_bookings": past,
        "upcoming_bookings": upcoming
    })

@bp.route('/cancel-booking/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def cancel_booking(booking_id):
    user_id = int(get_jwt_identity())
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"msg": "Booking not found"}), 404

    if booking.user_id != user_id:
        return jsonify({"msg": "Unauthorized"}), 403

    db.session.delete(booking)
    db.session.commit()
    return jsonify({"msg": "Booking cancelled"}), 200

