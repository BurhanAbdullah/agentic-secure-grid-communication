import time
import os
import sys

# Ensure v2_model is in the path
sys.path.append(os.getcwd())

from v2_model.core.crypto.ca_v2 import ROOT_CA_V2
from v2_model.agents.secure_agent_v2 import AgentV2

def run_v2_validation():
    print("\n=== AEGIS-GRID V2.0 SEPARATE MODEL AUDIT ===")
    
    # 1. PQ-Resilience Check
    node = "IISc_BANGALORE_NODE_01"
    sig = ROOT_CA_V2.issue_node_cert(node)
    print(f"PQ-Identity (Lattice-Sim): {'✅ VERIFIED' if ROOT_CA_V2.verify_cert(node, sig) else '❌ FAIL'}")

    # 2. Time-Bounded Check
    agent = AgentV2(os.urandom(32))
    print(f"Time-Bounded Policy:     {'✅ ACTIVE' if agent.is_fresh(time.time() - 0.5) else '❌ FAIL'}")
    
    # 3. Safety Check
    agent.update_pressure(6.0)
    print(f"V2 Safety Sink:          {'✅ LOCKED' if agent.locked else '❌ FAIL'}")
    print("============================================\n")

if __name__ == "__main__":
    run_v2_validation()
