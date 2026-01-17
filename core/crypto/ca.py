import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class GridCA:
    """Objective 12: High-Assurance Certification Authority"""
    def __init__(self):
        # In a real system, these would be loaded from a HSM (Hardware Security Module)
        self._private_key = RSA.generate(2048)
        self.public_key = self._private_key.publickey()

    def issue_node_certificate(self, node_id):
        """Signs a node's identity using the Root Private Key"""
        h = SHA256.new(node_id.encode())
        signature = pkcs1_15.new(self._private_key).sign(h)
        return signature

    def verify_certificate(self, node_id, signature):
        """Proof of Authenticity: Node must prove it holds the CA's signature"""
        h = SHA256.new(node_id.encode())
        try:
            pkcs1_15.new(self.public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

# Singleton instance for the architectural simulation
ROOT_CA = GridCA()
