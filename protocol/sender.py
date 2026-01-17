import os
from core.crypto import CryptoEngine
from core.fragmentation import fragment_message
from core.key_schedule import derive_layer_keys

def generate_traffic(agent, message: bytes, dummy_ratio: float):
    crypto = CryptoEngine()
    nonce = os.urandom(16)
    agent.last_nonce = nonce

    # Idle traffic indistinguishable
    if message is None:
        message = os.urandom(256)

    keys = derive_layer_keys(agent.master_key, nonce)

    data = message
    for k in keys:
        data = crypto.encrypt(data, k)

    packets = fragment_message(
        data,
        agent.fragment_count,
        dummy_ratio
    )

    agent.expected_real_fragments = agent.fragment_count
    return packets
