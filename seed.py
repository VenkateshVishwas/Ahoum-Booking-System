from app import create_app, db
from app.models import Facilitator, Event
from datetime import datetime, timedelta, timezone

app = create_app()

with app.app_context():
    # Optional: Drop and recreate tables
    # db.drop_all()
    db.create_all()

    if Facilitator.query.first():
        print("⚠️ Database already seeded.")
    else:
        # Sample Facilitators
        f1 = Facilitator(name="Ananya Sharma", crm_id="crm123")
        f2 = Facilitator(name="Ravi Kumar", crm_id="crm456")
        f3 = Facilitator(name="Meera Joshi", crm_id="crm789")

        db.session.add_all([f1, f2, f3])
        db.session.commit()

        # Use timezone-aware UTC now
        now = datetime.now(timezone.utc)

        # Sample Events with lat/lng
        events = [
            Event(
                title="Mindfulness Retreat",
                description="A weekend retreat for meditation and relaxation.",
                date=now + timedelta(days=7),
                location="Rishikesh",
                latitude=30.0869,
                longitude=78.2676,
                facilitator_id=f1.id,
                type="Meditation",
                status="scheduled",
                is_deleted=False
            ),
            Event(
                title="Yoga and Wellness",
                description="Morning yoga sessions with Ayurvedic meals.",
                date=now + timedelta(days=14),
                location="Goa",
                latitude=15.2993,
                longitude=74.1240,
                facilitator_id=f2.id,
                type="Yoga",
                status="scheduled",
                is_deleted=False
            ),
            Event(
                title="Evening Breathwork",
                description="Daily breathwork to reduce stress.",
                date=now + timedelta(days=3),
                location="Delhi",
                latitude=28.6139,
                longitude=77.2090,
                facilitator_id=f3.id,
                type="Breathwork",
                status="scheduled",
                is_deleted=False
            ),
            Event(
                title="Silent Sitting Session",
                description="1-hour silent mindfulness sitting.",
                date=now - timedelta(days=2),
                location="Online",
                latitude=0.0,  # neutral for online
                longitude=0.0,
                facilitator_id=f1.id,
                type="Meditation",
                status="completed",
                is_deleted=False
            ),
            Event(
                title="Weekend Detox Camp",
                description="Cleanse and reset with guided detox routines.",
                date=now + timedelta(days=10),
                location="Kerala",
                latitude=10.8505,
                longitude=76.2711,
                facilitator_id=f2.id,
                type="Detox",
                status="scheduled",
                is_deleted=False
            ),
            Event(
                title="Cancelled Yoga Session",
                description="This session has been cancelled.",
                date=now + timedelta(days=5),
                location="Mumbai",
                latitude=19.0760,
                longitude=72.8777,
                facilitator_id=f2.id,
                type="Yoga",
                status="cancelled",
                is_deleted=True
            ),
        ]

        db.session.add_all(events)
        db.session.commit()
        print("✅ Seeded facilitators and extended event data with coordinates!")
