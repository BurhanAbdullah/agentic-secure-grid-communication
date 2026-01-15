import os
from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys
from core.fragmentation import fragment_message

def generate_traffic(agent, message: bytes, dummy_ratio: float):
    crypto = CryptoEngine()

    # ===============================
    # IDLE TRAFFIC (NO REAL MESSAGE)
    # ===============================
    if message is None:
        n_fragments = agent.fragment_count
        dummy_payload = b"\x00" * 32
        packets = fragment_message(
            dummy_payload,
            n_fragments,
            dummy_ratio,
            agent.master_key,
            force_dummy=True
        )
        return packets

    # ===============================
    # REAL MESSAGE TRAFFIC
    # ===============================
    nonce = os.urandom(16)
    agent.last_nonce = nonce
    keys = derive_layer_keys(agent.master_key, nonce)

    data = message
    for k in keys:
        data = crypto.encrypt(data, k)

    n_fragments = agent.fragment_count
    packets = fragment_message(
        data,
        n_fragments,
        dummy_ratio,
        agent.master_key
    )

    agent.expected_real_fragments = sum(not p.is_dummy for p in packets)
    return packets
