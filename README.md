# Aegis-Grid v1.1
### Resilient Agentic Communication for Critical Infrastructure

Aegis-Grid is a high-integrity communication protocol designed to maintain Smart Grid stability during coordinated Cyber-Physical attacks. It utilizes **Agentic Thresholding** and **Cumulative Attack Pressure (CAP)** to distinguish between network congestion and active command forgery.

## 🛡️ Core Innovation: The 12-Objective Framework
1. **17-Layer Cryptic Architecture:** Multi-fragment data dispersal.
2. **Indistinguishable Dummies:** Signed dummy packets prevent traffic analysis.
3. **Per-Layer Key Separation:** HMAC-SHA256 derivation per fragment.
4. **Adaptive Thresholding:** Dynamic quorums based on real-time network entropy.
5. **Irreversible Time-Lock:** Permanent fail-secure lockout upon integrity depletion.
... (and the rest of your 12 objectives)

## 📊 Empirical Validation
Under a stress test of **40% Network Loss** and **60% Forgery Injection**, Aegis-Grid demonstrated:
- **Resilience:** Legitimate command survival until trust quorums were depleted.
- **Fail-Secure:** 100% rejection of malicious commands through autonomous Node Locking.

## 🛠️ Usage
```bash
python3 main.py
pip install pycryptodome
cat > core/crypto/encryption.py << 'EOF'
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class AegisCrypt:
    def __init__(self, key):
        self.key = key # Master Key
    
    def encrypt_payload(self, data):
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, cipher.nonce, tag

    def decrypt_payload(self, ciphertext, nonce, tag):
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)
