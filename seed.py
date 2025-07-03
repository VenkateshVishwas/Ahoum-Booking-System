from app import create_app, db
from app.models import Facilitator, Event
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Optional: Drop and recreate tables
    # db.drop_all()
    db.create_all()

    # Check if already seeded
    if Facilitator.query.first():
        print("⚠️ Database already seeded.")
    else:
        # Sample Facilitators
        f1 = Facilitator(name="Ananya Sharma", crm_id="crm123")
        f2 = Facilitator(name="Ravi Kumar", crm_id="crm456")

        db.session.add_all([f1, f2])
        db.session.commit()

        # Sample Events
        e1 = Event(
            title="Mindfulness Retreat",
            description="A weekend retreat for meditation and relaxation.",
            date=datetime.utcnow() + timedelta(days=7),
            location="Rishikesh",
            facilitator_id=f1.id
        )

        e2 = Event(
            title="Yoga and Wellness",
            description="Morning yoga sessions with Ayurvedic meals.",
            date=datetime.utcnow() + timedelta(days=14),
            location="Goa",
            facilitator_id=f2.id
        )

        db.session.add_all([e1, e2])
        db.session.commit()

        print("✅ Seeded sample facilitators and events!")
