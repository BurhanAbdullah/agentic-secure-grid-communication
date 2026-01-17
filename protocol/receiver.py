from core.signature import SignatureEngine
def receive_and_reconstruct(packets, agent):
    if agent.is_locked() or not packets: return False
    v = SignatureEngine()
    seen, forgeries = set(), 0
    
    for p in packets:
        # Obj 3: Enforce per-layer key separation
        layer_key = agent.get_layer_key(p.frag_id)
        if v.verify(p.signable(), p.signature, layer_key):
            seen.add(p.frag_id)
        else:
            forgeries += 1
    
    agent.observe(loss=0, forgery_detected=(forgeries > 0))
    return len(seen) >= agent.threshold