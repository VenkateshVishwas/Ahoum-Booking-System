## 💳 Razorpay Payment Integration

We have designed a complete plan for integrating Razorpay into the Ahoum Booking System to securely collect payments during event bookings.

---

### ✅ Integration Workflow

1. **Setup Razorpay**
   - Create an account and generate API keys.
   - Add these to your `.env`:
     ```env
     RAZORPAY_KEY_ID=your_key_id
     RAZORPAY_KEY_SECRET=your_key_secret
     ```

2. **Install SDK**
   ```bash
   pip install razorpay
   ```

3. **Update Booking Model**
   ```python
   is_paid = db.Column(db.Boolean, default=False)
   payment_id = db.Column(db.String(100))
   amount_paid = db.Column(db.Float)
   ```

4. **Create Razorpay Order**
   Endpoint: `POST /create-payment`
   ```python
   order = razorpay_client.order.create({
       "amount": amount * 100,
       "currency": "INR",
       "payment_capture": 1
   })
   ```

5. **Confirm Booking**
   Endpoint: `POST /confirm-booking`
   ```python
   Booking(
       user_id=user_id,
       event_id=data['event_id'],
       is_paid=True,
       payment_id=data['payment_id'],
       amount_paid=data['amount']
   )
   ```

6. **Optional Webhook**
   Use `/payment-webhook` for payment success, failure, or refund events.

---

### 🔍 Razorpay API Overview

| Method | Description         |
|--------|---------------------|
| GET    | Retrieve data       |
| POST   | Create resource     |
| PUT    | Replace resource    |
| DELETE | Delete resource     |
| PATCH  | Partial update      |

**Common Data Types:**  
- `String`, `Integer`, `Float`, `Boolean`, `Array`, `Object`

**Status Codes:**  
- 2xx Success, 4xx Client Error, 5xx Server Error

**Rate Limits:**  
- Handle 429 with exponential backoff.

**Pagination Example:**  
```http
GET /payments?count=10&skip=10
```

---

### 📊 Future Enhancements

- Razorpay dashboard integration
- Refunds and retries
- Email receipts to users
- Admin reporting with filters