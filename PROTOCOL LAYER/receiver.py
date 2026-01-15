from core.timing import within_time_window

def receiver_pipeline(packets, agent, time_window_ms):
    valid = []
    for p in packets:
        if not within_time_window(p.timestamp, time_window_ms):
            return False
        if not p.is_dummy:
            valid.append(p)
    return agent.verify(valid) and len(valid) > 0
