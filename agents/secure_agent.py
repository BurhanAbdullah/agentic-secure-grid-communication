class SecureAgent:
    def __init__(self, master_key):
        self.master_key = master_key
        self.threat_score = 0.0
        self.expected_real_fragments = 0
        self.last_nonce = None

        # --- NEW ---
        self.fragment_count = 8
        self.reconstruction_threshold = 0.7  # 70%

    def update(self, loss, delay):
        self.threat_score = min(1.0, 0.7*self.threat_score + 0.3*(loss + delay))
        self.fragment_count = 8 + int(4 * self.threat_score)

    def can_reconstruct(self, received_real):
        required = int(self.reconstruction_threshold * self.expected_real_fragments)
        return received_real >= required
