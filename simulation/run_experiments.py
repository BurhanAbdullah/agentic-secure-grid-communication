import time
import random

def run_all(agent, generate_fn, receive_fn):
    print("\n=== Adaptive Threshold + Time-Lock under DDoS ===")

    for loss in [0.1, 0.2, 0.3, 0.4]:
        success = 0
        agent.attack_score = 0.0
        agent.attack_start = None
        agent.locked = False

        for _ in range(50):
            now = time.time()
            agent.observe(loss, now)

            packets = generate_fn(agent, b"Shutdown Station A", 1.0)
            kept = [p for p in packets if random.random() > loss]

            if receive_fn(kept, agent):
                success += 1

            if agent.is_locked():
                break

        print(
            f"Loss {loss:.1f} → Threshold {agent.threshold} "
            f"→ Reconstruction Prob {success/50:.3f} "
            f"→ {'LOCKED' if agent.is_locked() else 'ACTIVE'}"
        )
