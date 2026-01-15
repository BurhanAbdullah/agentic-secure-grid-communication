from dataclasses import dataclass
import time
import uuid

@dataclass(frozen=True)
class Packet:
    packet_id: str
    payload: bytes
    is_dummy: bool
    timestamp: float
    auth_tag: str

    @staticmethod
    def create(payload: bytes, is_dummy: bool):
        return Packet(
            packet_id=str(uuid.uuid4()),
            payload=payload,
            is_dummy=is_dummy,
            timestamp=time.time(),
            auth_tag="VALID"
        )
