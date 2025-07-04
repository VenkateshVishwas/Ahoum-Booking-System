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
### 🔐 Payment Verification via Razorpay API (Backend)

Currently, the frontend sends the payment status to the backend. For a more secure flow, we should verify the payment using Razorpay's SDK on the backend.

#### ✅ Recommended Flow:

1. After successful payment on the frontend, send the following to your backend:
   - `razorpay_order_id`
   - `razorpay_payment_id`
   - `razorpay_signature`

2. On the backend, use Razorpay's utility method to verify the signature:

   ```python
   razorpay_client.utility.verify_payment_signature({
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   })
3. You can pass metadata like `user_id` or `event_title` when creating a Razorpay order using the `notes` parameter.

This metadata is:

- Visible on the Razorpay Dashboard
- Automatically included in webhook payloads

#### ✅ Example:

```python
notes = {
  "user_id": user_id,
  "event_title": event.title
}

order = razorpay_client.order.create({
    "amount": amount * 100,
    "currency": "INR",
    "payment_capture": 1,
    "notes": notes
})
```


**Optional Webhook (Recommended)**  
   Use `/payment-webhook` to handle automatic updates from Razorpay like:
   - `payment.captured` (successful payment)
   - `payment.failed`
   - `refund.processed`

   **Implementation Tip**:  
   ✅ Verify signature using Razorpay's SDK:

   ```python
   razorpay.utility.verify_webhook_signature(
       request_body,  # raw body from Razorpay
       received_signature,  # from header: X-Razorpay-Signature
       webhook_secret  # your webhook secret from Razorpay dashboard
   )
   ```

---

### 📊 Future Enhancements

- Razorpay dashboard integration
- Refunds and retries
- Email receipts to users
- Admin reporting with filters