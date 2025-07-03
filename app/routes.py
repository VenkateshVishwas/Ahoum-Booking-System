from flask import Blueprint, request, jsonify
from . import db
from .models import User, Event, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime
from .crm import notify_crm
from math import radians, cos, sin, asin, sqrt
import os, requests
from dotenv import load_dotenv



bp = Blueprint('main', __name__)

def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in km
    return c * r

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
    query = Event.query.filter_by(is_deleted=False)

    # Optional filters
    status = request.args.get('status')
    event_type = request.args.get('type')

    if status:
        query = query.filter_by(status=status)
    if event_type:
        query = query.filter_by(type=event_type)

    events = query.all()
    output = []
    for e in events:
        output.append({
            'id': e.id,
            'title': e.title,
            'description': e.description,
            'date': e.date.isoformat(),
            'location': e.location,
            'facilitator': e.facilitator.name,
            'status': e.status,
            'type': e.type
        })
    return jsonify({'events': output})


@bp.route('/events/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    data = request.get_json()
    event = Event.query.get(event_id)

    if not event or event.is_deleted:
        return jsonify({'msg': 'Event not found'}), 404

    # Optional: add admin check here
    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)
    event.date = datetime.fromisoformat(data.get('date')) if data.get('date') else event.date
    event.location = data.get('location', event.location)
    event.status = data.get('status', event.status)

    db.session.commit()
    return jsonify({'msg': 'Event updated'}), 200


@bp.route('/events/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Event.query.get(event_id)

    if not event or event.is_deleted:
        return jsonify({'msg': 'Event not found'}), 404

    # Soft delete
    event.is_deleted = True
    event.status = "cancelled"
    db.session.commit()
    return jsonify({'msg': 'Event cancelled'}), 200


# -------- BOOKING --------

@bp.route('/book', methods=['POST'])
@jwt_required()
def book_event():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    event = Event.query.get(data['event_id'])

    if not event or event.is_deleted or event.status != "scheduled":
        return jsonify({'msg': 'Event not available'}), 404

    new_booking = Booking(user_id=user_id, event_id=event.id)
    db.session.add(new_booking)
    db.session.commit()

    notify_crm(booking=new_booking)
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
        if event.is_deleted:
            continue

        facilitator = event.facilitator
        event_data = {
            "booked_at": b.booked_at.isoformat(),
            "event": {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date.isoformat(),
                "location": event.location,
                "facilitator": facilitator.name,
                "status": event.status
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


@bp.route('/events/nearby', methods=['GET'])
@jwt_required()
def get_nearby_events():
    try:
        user_lat = float(request.args.get("lat"))
        user_lng = float(request.args.get("lng"))
        radius = float(request.args.get("radius", 10))  # default to 10 km
    except (TypeError, ValueError):
        return jsonify({"msg": "lat, lng and optional radius (km) are required as query params."}), 400

    events = Event.query.filter_by(is_deleted=False, status="scheduled").all()
    results = []

    for e in events:
        if e.latitude and e.longitude:
            dist = haversine(user_lat, user_lng, e.latitude, e.longitude)
            if dist <= radius:
                results.append({
                    "id": e.id,
                    "title": e.title,
                    "location": e.location,
                    "date": e.date.isoformat(),
                    "distance_km": round(dist, 2),
                    "facilitator": e.facilitator.name,
                    "type": e.type
                })

    return jsonify({"nearby_events": results})
