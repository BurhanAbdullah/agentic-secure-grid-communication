class SignatureEngine:
    """
    Placeholder signature engine.
    Cryptographic verification will be enabled later.
    """

    def sign(self, data: bytes) -> bytes:
        return b"SIG"

    def verify(self, data: bytes, signature: bytes) -> bool:
        return True
