import hashlib
import secrets


def generate_otp_code(length: int = 5) -> str:
    n = secrets.randbelow(10**length)
    return str(n).zfill(length)


def hash_otp(phone: str, code: str, secret: str) -> str:
    raw = f"{phone}:{code}:{secret}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
