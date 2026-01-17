class SecureAgent:
    def __init__(self, master_key):
        self.master_key = master_key

        # Threat tracking
        self.attack_score = 0.0

        # Fragment parameters
        self.base_fragments = 12
        self.fragment_count = self.base_fragments
        self.threshold = self.base_fragments
        self.threshold = self.base_fragments

        # Protocol state
        self.expected_real_fragments = 0
        self.last_nonce = None

        # Irreversible lock
        self.locked = False
        self.lock_reason = None

    def observe(self, loss_rate: float):
        # Accumulate attack pressure
        self.attack_score = min(1.0, self.attack_score + loss_rate)

        # Adaptive threshold (never below 60%)
        min_threshold = int(0.6 * self.fragment_count)
        adaptive = int(self.fragment_count * (1.0 - self.attack_score))

        self.threshold = max(min_threshold, adaptive)

    def is_locked(self):
        return self.locked
