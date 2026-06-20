from flask import Flask, request, jsonify
from vapid_utils import load_vapid_public_key
from flask_cors import CORS
from pywebpush import webpush, WebPushException
import json, os

SUBS_FILE = "subscriptions.json"

def load_subscriptions():
    if os.path.exists(SUBS_FILE):
        try:
            with open(SUBS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_subscriptions(subs):
    with open(SUBS_FILE, "w") as f:
        json.dump(subs, f)

app = Flask(__name__)
CORS(app)
subscriptions = load_subscriptions()

@app.route("/")
def home():
    return "Hello Tino"

@app.route("/submit", methods=["POST"])
def info():
    data = request.json
    if "name" not in data:
        return jsonify({"error": "Missing field: name"}), 400
    if "age" not in data:
        return jsonify({"error": "Missing field: age"}), 400
    return jsonify({"status": "ok", "user": data["name"]})

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    try:
        endpoint = data["endpoint"]
        p256dh = data["keys"]["p256dh"]
        auth = data["keys"]["auth"]
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

    new_sub = {
        "endpoint": endpoint,
        "keys": {
            "p256dh": p256dh,
            "auth": auth
        }
    }

    if not any(s["endpoint"] == endpoint for s in subscriptions):
        subscriptions.append(new_sub)
        save_subscriptions(subscriptions)

    print("New subscription:", new_sub)
    return jsonify({"status": "subscribed"})

@app.route("/send", methods=["POST"])
def send_notification():
    payload = request.json.get("message", "Hello!")
    results = {"sent": 0, "failed": 0}

    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=payload.encode("utf-8"),
                vapid_private_key="private_key.pem",
                vapid_claims={"sub": "mailto:54351463+tzuvela@users.noreply.github.com"}
            )
            results["sent"] += 1
        except Exception as e:
            print("Push failed:", e)
            results["failed"] += 1

    return jsonify(results)

@app.route("/vapidPublicKey")
def vapid_public_key():
    return jsonify({"publicKey": load_vapid_public_key()})

if __name__ == "__main__":
    app.run(use_reloader=False)
