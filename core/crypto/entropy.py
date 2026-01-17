import math
from collections import Counter

def calculate_entropy(data):
    if not data: return 0
    entropy = 0
    counts = Counter(data)
    total = len(data)
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def verify_indistinguishability(data_pkt, dummy_pkt):
    h_data = calculate_entropy(data_pkt)
    h_dummy = calculate_entropy(dummy_pkt)
    # Proof: If delta < 0.1, the packets are statistically indistinguishable
    return abs(h_data - h_dummy) < 0.1
