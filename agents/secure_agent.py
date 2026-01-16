class SecureAgent:
    def __init__(self, master_key):
        self.master_key = master_key

        # Security state
        self.threat_score = 0.0
        self.attack_score = 0.0

        # Fragment & protocol state
        self.base_fragments = 8
        self.fragment_count = 8
        self.expected_real_fragments = 0
        self.last_nonce = None

        # Irreversible lock
        self.locked = False
        self.lock_reason = None

    def observe(self, loss=0.0, delay=0.0):
        """
        Adaptive but bounded defense escalation.
        """
        pressure = loss + delay
        self.attack_score += pressure
        self.threat_score = min(1.0, self.threat_score + 0.2 * pressure)

        # 🧠 Controlled adaptation (NO PANIC)
        self.fragment_count = int(
            self.base_fragments + 2 * self.threat_score
        )

        # Absolute safety bounds
        self.fragment_count = max(6, min(10, self.fragment_count))

        # Irreversible lock ONLY on sustained attack
        if self.attack_score > 4.0 and not self.locked:
            self.locked = True
            self.lock_reason = "IRREVERSIBLE_ATTACK_THRESHOLD_EXCEEDED"

    def is_locked(self):
        return self.locked
