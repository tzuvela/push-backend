from cryptography.hazmat.primitives import serialization
from pathlib import Path
import base64

def load_vapid_public_key():
    pem_data = Path("public_key.pem").read_bytes()
    public_key = serialization.load_pem_public_key(pem_data)
    raw_key = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    return base64.urlsafe_b64encode(raw_key).rstrip(b"=").decode("utf-8")