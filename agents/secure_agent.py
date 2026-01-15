class SecureAgent:
    def __init__(self, master_key):
        self.master_key = master_key

        # Threat state
        self.loss = 0.0
        self.delay = 0.0
        self.ddos_pressure = 0.0

        # Adaptive parameters
        self.fragment_count = 8
        self.dummy_ratio = 1.0
        self.required_fraction = 0.75

        # Time-lock state
        self.locked = False
        self.last_nonce = None
        self.expected_real_fragments = 0

    def observe(self, loss, delay, arrival_skew):
        self.loss = loss
        self.delay = delay
        self.ddos_pressure = min(1.0, loss + delay + arrival_skew)
        self._adapt()

    def _adapt(self):
        self.fragment_count = int(8 + 8 * self.ddos_pressure)
        self.dummy_ratio = 1.0 + 2.0 * self.ddos_pressure
        self.required_fraction = max(0.5, 0.9 - 0.4 * self.ddos_pressure)

    def threshold(self):
        return int(self.expected_real_fragments * self.required_fraction)

    def trigger_lock(self):
        self.locked = True
