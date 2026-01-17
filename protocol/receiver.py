import time
from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys
from core.signature import SignatureEngine

def receive_and_reconstruct(packets, agent, time_window_ms=50):
    if agent.is_locked():
        return None

    if not packets:
        return None

    now = time.time()
    verifier = SignatureEngine()

    valid = []

    for p in packets:
        if (now - p.timestamp) * 1000 > time_window_ms:
            agent.observe(0.1, now)
            continue

        if not verifier.verify(p.payload, p.signature):
            agent.locked = True
            agent.lock_reason = "SIGNATURE_FORGERY"
            return None

        if not p.is_dummy:
            valid.append(p)

    if len(valid) < agent.threshold:
        agent.observe(0.1, now)
        return None

    return b"RECONSTRUCTED"
