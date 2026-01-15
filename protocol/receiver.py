from core.timing import within_time_window
from core.crypto import CryptoEngine
from core.key_schedule import derive_layer_keys

def receive_and_reconstruct(packets, agent, time_window_ms=50):
    """
    Receiver pipeline:
    - time validity check
    - dummy filtering
    - fragment completeness check
    - multilayer decryption
    """

    crypto = CryptoEngine()

    # Safety: no packets
    if not packets:
        return None

    # Time-bound correctness
    for p in packets:
        if not within_time_window(p.timestamp, time_window_ms):
            return None

    # Extract real fragments
    real_packets = [p for p in packets if not p.is_dummy]

    # Require enough fragments
    if len(real_packets) < agent.expected_real_fragments:
        return None

    # Reassemble payload
    data = b"".join(p.payload for p in real_packets)

    # Multilayer decryption (reverse order)
    keys = derive_layer_keys(agent.master_key, agent.last_nonce)
    for k in reversed(keys):
        data = crypto.decrypt(data, k)

    return data
