from core.fragmentation import fragment_message

def sender_pipeline(message, agent, threat):
    params = agent.adapt(threat)
    return fragment_message(
        message.encode(),
        params["fragments"],
        params["dummy_ratio"]
    )
