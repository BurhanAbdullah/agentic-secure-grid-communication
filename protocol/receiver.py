import time
from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys
from core.signature import SignatureEngine

def receive_and_reconstruct(packets, agent, time_window_ms=50):
    if agent.locked:
        return None

    if not packets:
        return None

    now = time.time()
    crypto = CryptoEngine()
    verifier = SignatureEngine()

    valid_fragments = []

    for p in packets:
        if (now - p.timestamp) * 1000 > time_window_ms:
            agent.locked = True
            agent.lock_reason = "TIME_WINDOW_EXCEEDED"
            return None

        if p.is_dummy:
            continue

        if not verifier.verify(p.payload, p.signature, agent.master_key):
            agent.locked = True
            agent.lock_reason = "SIGNATURE_FORGERY_DETECTED"
            return None

        valid_fragments.append(p.payload)

    if len(valid_fragments) < agent.threshold:
        return None

    data = b"".join(valid_fragments)

    keys = derive_layer_keys(agent.master_key, agent.last_nonce)
    for k in reversed(keys):
        data = crypto.decrypt(data, k)

    return data
