import random
from core.packet import Packet

def fragment_message(data: bytes, n_fragments: int, dummy_ratio: float):
    fragments = []

    # === FORCE exact number of REAL fragments ===
    chunk_size = max(1, len(data) // n_fragments)
    padded = data.ljust(chunk_size * n_fragments, b'\x00')

    for i in range(n_fragments):
        frag = padded[i*chunk_size:(i+1)*chunk_size]
        fragments.append(Packet.create(frag, False, b"REAL_SIG"))

    # === Dummy fragments ===
    dummy_count = int(n_fragments * dummy_ratio)
    for _ in range(dummy_count):
        fragments.append(Packet.create(b'\x00' * chunk_size, True, b"DUMMY_SIG"))

    random.shuffle(fragments)
    return fragments
