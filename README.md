# Ahoum Booking API

This is a Flask-based backend API for a wellness booking system, built for the Ahoum Backend Developer Assignment.

## 🚀 Features

- User Registration & Login (JWT Authentication)
- View Available Events (Sessions)
- Book Events (Linked to Facilitators from CRM)
- View Upcoming & Past Bookings
- Cancel Bookings
- CRM Notification Webhook (Simulated via Logging)

---

## 📦 Tech Stack

- **Flask** & Flask-JWT-Extended
- **SQLAlchemy** ORM
- **SQLite** (default) or MySQL compatible
- `.env` based configuration
- Postman Collection for API testing

---

## 🧑‍💻 Setup Instructions

### 1. Clone & Install

```bash
git clone https://github.com/your-username/ahoum-backend.git
cd ahoum-backend
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in root:

```env
SECRET_KEY=super-secret
JWT_SECRET_KEY=jwt-secret
DATABASE_URI=sqlite:///ahoum.db
```

### 3. Create Tables

```bash
python run.py
# or alternatively
python seed.py  # to also add dummy facilitators & events
```

---

## 🧪 API Endpoints

| Method | Endpoint             | Description                  |
|--------|----------------------|------------------------------|
| POST   | `/register`          | Register a new user          |
| POST   | `/login`             | Get JWT token                |
| GET    | `/events`            | List all events              |
| POST   | `/book`              | Book an event (requires token) |
| GET    | `/my-bookings`       | View past and upcoming bookings |
| DELETE | `/cancel-booking/<id>` | Cancel a booking            |

> All protected routes require `Authorization: Bearer <token>` header.

---

## 🔔 CRM Notification (Simulated)

When a booking is made, the system logs a payload like:

```json
{
  "booking_id": 1,
  "user": { "id": 1, "name": "Test User" },
  "event": { "id": 1, "title": "Mindfulness Retreat" },
  "facilitator": { "id": 1, "crm_id": "crm123" }
}
```

Located in: `app/crm.py`

---

## 📬 Postman Collection

Import the file [`Ahoum_Booking_API.postman_collection.json`](./Ahoum_Booking_API.postman_collection.json) in Postman.

Set an environment variable:
```json
{ "token": "your_jwt_token_here" }
```

---

## 📘 To-Do (Optional Enhancements)

- Replace SQLite with MySQL for deployment
- Add pagination to bookings
- Add time-based cancellation restrictions

---

## 👤 Author

- [Your Name] – Full Stack Developer