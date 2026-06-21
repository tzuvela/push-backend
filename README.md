# Web Push Notification Backend (Flask)

Minimal API for sending Web Push notifications to subscribed browsers.  
Designed to work with a static frontend (e.g., Netlify) and a service worker that displays notifications.

# Features

Stores browser push subscriptions
Sends Web Push notifications using VAPID keys
Simple Flask API with two endpoints:

- POST /subscribe — store a subscription
- POST /send — send a notification to all subscribers

# Requirements

Python 3.10+
Flask
pywebpush

- VAPID keys (public + private)

Install dependencies:

pip install -r requirements.txt
Environment Variables
Create a .env file or export the following:

Code
VAPID_PUBLIC_KEY=your_public_key
VAPID_PRIVATE_KEY=your_private_key
Running the Server
bash
python main.py
The backend will start on:

Code
http://localhost:5000
API Endpoints
POST /subscribe
Stores a push subscription.

Body example:

json
{
"endpoint": "...",
"keys": {
"p256dh": "...",
"auth": "..."
}
}
POST /send
Sends a push notification to all stored subscribers.

Body example:

json
{
"message": "Hello from backend!"
}
Sending Notifications
The backend uses pywebpush to send notifications:

python
webpush(
subscription_info=sub,
data=message,
vapid_private_key=VAPID_PRIVATE_KEY,
vapid_claims={"sub": "mailto:admin@example.com"}
)
Notes
Subscriptions are stored in memory for simplicity.

For production, store in a database.

Works with Netlify + Render deployments.
