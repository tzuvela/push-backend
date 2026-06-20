import requests

payload = {"name": "Tino", "age": 30}
response = requests.post("http://127.0.0.1:5000/submit", json=payload)
print(response.json())


sub = {
    "endpoint": "https://example.com/123",
    "keys": {
        "p256dh": "abc",
        "auth": "xyz"
        
    }
}

r = requests.post("http://127.0.0.1:5000/subscribe", json=sub)
print(r.json())