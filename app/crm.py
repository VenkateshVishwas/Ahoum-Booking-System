import requests
from flask import current_app
from .models import User, Event, Facilitator, Booking

def notify_crm(booking: Booking):
    try:
        user = booking.user
        event = booking.event
        facilitator = event.facilitator

        payload = {
            "booking_id": booking.id,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
            },
            "event": {
                "id": event.id,
                "title": event.title,
                "date": event.date.isoformat()
            },
            "facilitator": {
                "id": facilitator.id,
                "name": facilitator.name,
                "crm_id": facilitator.crm_id
            }
        }

        # Simulated CRM endpoint (replace with real one later)
        # crm_url = "https://example-crm.com/api/booking"

        # For demo, you can log instead of send
        current_app.logger.info(f"CRM Notification Payload: {payload}")

        # Uncomment below to send the actual request
        # response = requests.post(crm_url, json=payload)
        # response.raise_for_status()

        return True
    except Exception as e:
        current_app.logger.error(f"CRM Notification Failed: {e}")
        return False
