import time
import random
import numpy as np

def run_all(agent, generate_fn, receive_fn):
    print("\n=== Adaptive Threshold under DDoS ===")

    for loss in [0.1, 0.2, 0.3, 0.4]:
        success = 0

        for _ in range(50):
            packets = generate_fn(agent, b"Shutdown Station A", 1.0)

            arrival_skew = random.uniform(0.0, loss)

            agent.observe(
                loss=loss,
                delay=loss * 0.5,
                arrival_skew=arrival_skew
            )

            kept = [p for p in packets if random.random() > loss]

            if receive_fn(kept, agent):
                success += 1

        prob = success / 50.0
        print(f"Loss {loss:.1f} → Threshold {agent.threshold()} → Reconstruction Prob {prob:.3f}")
