from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import time

class AegisCrypt:
    def __init__(self, key):
        self.key = key
    
    def seal(self, data):
        start = time.perf_counter()
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        latency = time.perf_counter() - start
        return {
            "ciphertext": ciphertext,
            "nonce": cipher.nonce,
            "tag": tag,
            "latency": latency
        }

    def open(self, bundle):
        try:
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=bundle['nonce'])
            return cipher.decrypt_and_verify(bundle['ciphertext'], bundle['tag'])
        except:
            return None
