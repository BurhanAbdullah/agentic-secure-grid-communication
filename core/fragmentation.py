import random
from core.packet import Packet

def fragment_message(data: bytes, n_fragments: int, dummy_ratio: float):
    fragments = []
    size = max(1, len(data) // n_fragments)

    # Simple deterministic signature placeholder
    real_sig = b"REAL_SIG"
    dummy_sig = b"DUMMY_SIG"

    for i in range(n_fragments):
        frag = data[i*size:(i+1)*size]
        fragments.append(Packet.create(frag, False, real_sig))

    dummy_count = int(n_fragments * dummy_ratio)
    for _ in range(dummy_count):
        fragments.append(Packet.create(b'\x00' * size, True, dummy_sig))

    random.shuffle(fragments)
    return fragments
