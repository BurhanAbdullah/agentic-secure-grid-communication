import random
from core.packet import Packet

def fragment_message(data: bytes, n_fragments: int, dummy_ratio: float,
                     key: bytes, force_dummy=False):
    packets = []
    size = max(1, len(data) // n_fragments)

    # REAL FRAGMENTS
    if not force_dummy:
        for i in range(n_fragments):
            frag = data[i*size:(i+1)*size]
            packets.append(Packet.create(frag, False, key))

    # DUMMY FRAGMENTS
    dummy_count = int(n_fragments * (1 + dummy_ratio))
    for _ in range(dummy_count):
        packets.append(Packet.create(b"\x00"*size, True, key))

    random.shuffle(packets)
    return packets
