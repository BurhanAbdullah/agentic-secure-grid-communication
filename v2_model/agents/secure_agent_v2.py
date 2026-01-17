import hashlib
import time

class AgentV2:
    """V2: Time-Bounded Stochastic Controller"""
    PRESSURE_LIMIT = 5.5
    TIME_WINDOW = 2.0  # Seconds (Strict Time-Bounded Property)

    def __init__(self, master_key):
        self.master_key = master_key
        self.locked = False
        self.pressure = 0.0
        self.threshold = 12

    def is_fresh(self, packet_ts):
        """Validates the Time-Bounded constraint"""
        return (time.time() - packet_ts) < self.TIME_WINDOW

    def update_pressure(self, amount):
        if self.locked: return
        self.pressure += amount
        if self.pressure >= self.PRESSURE_LIMIT:
            self.locked = True
            print(f"[V2-ALERT] TERMINAL LOCKOUT: Pressure {self.pressure:.2f}")

    def get_pq_key(self, layer_id):
        """Post-Quantum KDF using SHA3-512"""
        return hashlib.sha3_512(self.master_key + str(layer_id).encode()).digest()
