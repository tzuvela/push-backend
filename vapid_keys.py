from pathlib import Path

PRIVATE_KEY = Path("private_key.pem").read_text()
PUBLIC_KEY = Path("public_key.pem").read_text()

VAPID_CLAIMS = {
    "sub": "mailto:54351463+tzuvela@users.noreply.github.com"
}