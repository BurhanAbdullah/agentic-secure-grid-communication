from core.signature import SignatureEngine
from core.packet import Packet
import os, random

def generate_traffic(agent, data, dummy_ratio):
    signer = SignatureEngine()
    msg_id = os.urandom(8)
    fragments = []
    size = max(1, len(data) // agent.fragment_count)

    for i in range(agent.fragment_count):
        frag = data[i*size:(i+1)*size]
        pkt = Packet.create(msg_id, i, agent.fragment_count, frag, False)
        # Obj 3: Use derived per-layer key
        layer_key = agent.get_layer_key(i)
        pkt.signature = signer.sign(pkt.signable(), layer_key)
        fragments.append(pkt)
    
    random.shuffle(fragments)
    return fragments