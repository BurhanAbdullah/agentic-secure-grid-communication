from core.timing import within_time_window
from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys

def receive_and_reconstruct(packets, agent, time_window_ms=50):
    crypto = CryptoEngine()

    if agent.locked:
        return None

    if not packets:
        agent.trigger_lock()
        return None

    for p in packets:
        if not within_time_window(p.timestamp, time_window_ms):
            agent.trigger_lock()
            return None

    real_packets = [p for p in packets if not p.is_dummy]

    if len(real_packets) < agent.threshold():
        return None

    data = b"".join(p.payload for p in real_packets)

    keys = derive_layer_keys(agent.master_key, agent.last_nonce)
    for k in reversed(keys):
        data = crypto.decrypt(data, k)

    return data
