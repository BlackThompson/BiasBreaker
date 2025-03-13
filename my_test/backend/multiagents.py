from agentscope.agents import DialogAgent
from agentscope.message import Msg
from agentscope import msghub
import agentscope
import time


def setup_conversation():
    # Initialize via model configuration for simplicity
    agentscope.init(
        model_configs={
            "config_name": "my-qwen-max",
            "model_name": "qwen-max",
            "model_type": "dashscope_chat",
            "api_key": "sk-1b3cfc6b76e74aa88b8be157001d1f58",
        },
    )

    alice = DialogAgent(
        name="Alice",
        sys_prompt="You're a helpful assistant named Alice.",
        model_config_name="my-qwen-max",
    )

    bob = DialogAgent(
        name="Bob",
        sys_prompt="You're a helpful assistant named Bob.",
        model_config_name="my-qwen-max",
    )

    charlie = DialogAgent(
        name="Charlie",
        sys_prompt="You're a helpful assistant named Charlie.",
        model_config_name="my-qwen-max",
    )

    return [alice, bob, charlie]


def get_agent_info(name):
    avatars = {
        "Alice": "https://api.dicebear.com/7.x/adventurer/svg?seed=Alice",
        "Bob": "https://api.dicebear.com/7.x/adventurer/svg?seed=Bob",
        "Charlie": "https://api.dicebear.com/7.x/adventurer/svg?seed=Charlie",
        "user": "https://api.dicebear.com/7.x/adventurer/svg?seed=user",
    }
    return {"name": name, "avatar": avatars.get(name, avatars["user"])}


def run_conversation(agents, message_queue):
    # Add system message
    greeting = Msg(
        name="user",
        content="Now you three count off each other from 1, and just report the number without any other information.",
        role="user",
    )

    # Send initial message
    message_queue.put(
        {
            "agent": get_agent_info("user"),
            "message": greeting.content,
            "timestamp": time.time(),
        }
    )

    with msghub(
        participants=agents,
        announcement=greeting,
    ) as hub:
        # First round
        for agent in agents[:3]:
            response = agent()
            message_queue.put(
                {
                    "agent": get_agent_info(agent.name),
                    "message": response.content,
                    "timestamp": time.time(),
                }
            )
            time.sleep(1)  # Add small delay for better UX

        # Remove Charlie
        hub.delete(agents[2])

        # Broadcast Charlie's departure
        departure_msg = Msg(
            "user",
            "Charlie has left the conversation.",
            "user",
        )
        hub.broadcast(departure_msg)

        message_queue.put(
            {
                "agent": get_agent_info("user"),
                "message": departure_msg.content,
                "timestamp": time.time(),
            }
        )

        time.sleep(1)

        # Second round
        for agent in agents[:2]:
            response = agent()
            message_queue.put(
                {
                    "agent": get_agent_info(agent.name),
                    "message": response.content,
                    "timestamp": time.time(),
                }
            )
            time.sleep(1)
