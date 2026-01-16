import hashlib

class SignatureEngine:
    """
    Lightweight signature abstraction.
    Replace with PQ signatures (Dilithium, Falcon) in production.
    """

    def sign(self, data: bytes, key: bytes) -> bytes:
        return hashlib.sha256(key + data).digest()

    def verify(self, data: bytes, signature: bytes, key: bytes) -> bool:
        expected = hashlib.sha256(key + data).digest()
        return expected == signature
