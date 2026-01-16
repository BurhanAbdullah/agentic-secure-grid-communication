import time
import random
import numpy as np

def run_all(agent, generate_fn, receive_fn):
    print("\n=== Adaptive Threshold under DDoS ===")

    for loss in [0.1, 0.2, 0.3, 0.4]:
        success = 0

        for _ in range(50):
            packets = generate_fn(agent, b"Shutdown Station A", 1.0)

            # Simulated delay pressure
            delay = random.uniform(0.0, loss)

            agent.observe(loss=loss, delay=delay)

            out = receive_fn(packets, agent)
            if out:
                success += 1

        print(
            f"Loss {loss:.1f} → Threshold {agent.fragment_count} → "
            f"Reconstruction Prob {success/50:.3f}"
        )
