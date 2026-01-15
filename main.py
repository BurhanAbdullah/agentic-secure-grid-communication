from simulation.run_experiments import run_all
from protocol.sender import generate_traffic
from protocol.receiver import receive_and_reconstruct
from agents.secure_agent import SecureAgent
from Crypto.Random import get_random_bytes

if __name__ == "__main__":
    key = get_random_bytes(16)
    agent = SecureAgent(key)

    run_all(
        agent,
        generate_traffic,
        receive_and_reconstruct
    )
