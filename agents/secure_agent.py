import hashlib

class SecureAgent:
    PRESSURE_LIMIT = 5.5

    def __init__(self, master_key):
        self.master_key = master_key
        self.locked = False
        self.pressure = 0.0
        self._lock_announced = False

        # Pillar 1 & 2: Structural Contract
        self.base_fragments = 12
        self.fragment_count = 12 
        self.threshold = 12

    def get_layer_key(self, layer_id):
        """Obj 3: Per-layer key separation"""
        return hashlib.sha256(self.master_key + str(layer_id).encode()).digest()

    def is_locked(self):
        return self.locked

    def observe(self, loss):
        """Obj 5: Adaptive Thresholding"""
        if self.locked: return
        # Adaptive Quorum adjustment
        self.threshold = max(4, int(self.base_fragments * (1.0 - loss)))
        
        # Pillar 2: Background pressure from channel noise
        if loss > 0.35:
            self.add_attack_pressure(0.15)

    def add_attack_pressure(self, amount):
        """Obj 6 & 8: CAP logic & Time-Lock Trigger"""
        if self.locked: return
        self.pressure += amount
        if self.pressure >= self.PRESSURE_LIMIT:
            self.locked = True
            if not self._lock_announced and __debug__:
                print(f"[SECURITY] TIME-LOCK irreversible failure -> Pressure: {self.pressure:.2f}")
                self._lock_announced = True
