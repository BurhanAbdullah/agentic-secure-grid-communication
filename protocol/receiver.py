from core.timing import within_time_window

def receive_and_reconstruct(packets, agent, time_window_ms=50):
    """
    Strict reconstruction:
    - All real fragments must arrive
    - All must be within time window
    - Any loss => permanent failure
    """

    real_packets = []

    for p in packets:
        if not within_time_window(p.timestamp, time_window_ms):
            return None
        if not p.is_dummy:
            real_packets.append(p)

    # 🔐 ALL-OR-NOTHING RULE
    if len(real_packets) != agent.expected_real_fragments:
        return None

    # Return reconstructed payload (symbolic)
    data = b"".join(p.payload for p in real_packets)
    return data
