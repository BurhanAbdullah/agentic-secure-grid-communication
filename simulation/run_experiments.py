import random
from simulation.adversary import inject_adversary

def run_all(agent, traffic_fn, receiver_fn):
    print("\n=== Aegis-Grid: v1.3 Triple-Pillar Validation ===")

    for loss in [0.1, 0.2, 0.3, 0.4]:
        success, locked, trials = 0, 0, 100

        for _ in range(trials):
            # Reset Agent for stateless trial
            agent.locked = False
            agent.pressure = 0.0
            agent._lock_announced = False

            # Pillar 2: Adaptive Observation
            agent.observe(loss)

            # Protocol Flow
            packets = traffic_fn(agent, b"POWER_GRID_CMD", 0.2)
            packets = inject_adversary(packets, forge_ratio=0.3)
            packets = [p for p in packets if random.random() > loss]

            if agent.is_locked():
                locked += 1
            elif receiver_fn(packets, agent):
                success += 1

        print(f"Loss {int(loss*100)}% | Success {success/trials:.3f} | Locked {locked/trials:.3f}")
