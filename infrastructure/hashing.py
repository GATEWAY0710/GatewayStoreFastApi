from typing import Tuple
import hashlib
import secrets

class HashingService:

    @staticmethod
    def hash_password(password: str) -> Tuple[str, str]:
        hash_salt = secrets.token_bytes(64)
        hash_object = hashlib.pbkdf2_hmac(
            "sha512",
            password.encode("utf-8"),
            hash_salt,
            10000,
        )
        return hash_salt.hex(), hash_object.hex()

    @staticmethod
    def validate_password(provided_password: str, stored_password_hash: str, stored_hash_salt: str) -> bool:
        ## hash proved password with store hash_salt
        provided_hash = hashlib.pbkdf2_hmac(
            "sha512",
            provided_password.encode("utf-8"),
            bytes.fromhex(stored_hash_salt),
            10000,
        )

        return provided_hash.hex() == stored_password_hash