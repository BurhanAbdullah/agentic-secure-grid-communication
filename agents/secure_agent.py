import hashlib
class SecureAgent:
    def __init__(self, master_key):
        self.master_key = master_key
        self.locked = False
        self.pressure = 0.0  # Obj 6: Pressure Accumulation
        self.base_fragments = 12
        self.fragment_count = 12 # Needed for sender
        self.threshold = 12      # Obj 5: Adaptive Threshold
        
    def get_layer_key(self, layer_id):
        # Obj 3: Per-layer key separation
        return hashlib.sha256(self.master_key + str(layer_id).encode()).digest()

    def observe(self, loss, forgery_detected=False):
        if self.locked: return
        
        # Obj 6 & 8: Pressure accumulation
        if forgery_detected:
            self.pressure += 1.2 
        elif loss > 0.35:
            self.pressure += 0.15
        else:
            self.pressure = max(0, self.pressure - 0.05)

        # Obj 5: Adaptive Threshold
        # Threshold increases as channel integrity (pressure) degrades
        self.threshold = max(4, min(12, int(12 * (1.0 - loss) + self.pressure)))

        # Obj 7: Permanent Lock
        if self.pressure > 4.0:
            self.locked = True
            print(f'[SECURITY] TIME-LOCK irreversible failure -> Pressure: {self.pressure:.2f}')

    def is_locked(self): return self.locked