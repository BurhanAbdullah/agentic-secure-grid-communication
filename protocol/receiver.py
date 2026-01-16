from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys
import time

def receive_and_reconstruct(packets, agent, time_window_ms=50):
    """
    Receiver with irreversible time-lock failure.
    """

    # Permanent lock
    if agent.is_locked():
        return None

    if not packets:
        return None

    now = time.time()
    crypto = CryptoEngine()

    # Time-lock enforcement
    for p in packets:
        delay_ms = (now - p.timestamp) * 1000
        if delay_ms > time_window_ms:
            agent.observe(loss=0.5, delay=delay_ms / 100.0)
            if agent.is_locked():
                return None

    # Filter real packets
    real = [p for p in packets if not p.is_dummy]

    if len(real) < agent.expected_real_fragments:
        agent.observe(loss=0.3, delay=0.0)
        return None

    # Reassemble
    data = b"".join(p.payload for p in real)

    # Multilayer decryption (symbolic)
    keys = derive_layer_keys(agent.master_key, agent.last_nonce)
    for k in reversed(keys):
        data = crypto.decrypt(data, k)

    return data
