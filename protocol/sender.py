import os
from core.fragmentation import fragment_message
from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys

def generate_traffic(agent, message: bytes, dummy_ratio: float):
    crypto = CryptoEngine()
    nonce = os.urandom(16)

    agent.last_nonce = nonce
    keys = derive_layer_keys(agent.master_key, nonce)

    # === CRITICAL FIX ===
    # Idle traffic must look EXACTLY like real traffic
    if message is None:
        message = os.urandom(256)

    data = message
    for k in keys:
        data = crypto.encrypt(data, k)

    packets = fragment_message(
        data,
        n_fragments=agent.fragment_count,
        dummy_ratio=dummy_ratio
    )

    agent.expected_real_fragments = sum(not p.is_dummy for p in packets)
    return packets
