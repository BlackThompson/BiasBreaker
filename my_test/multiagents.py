from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg
from agentscope import msghub
import agentscope

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

# Introduce the rule of the conversation
greeting = Msg(
    name="user",
    content="Now you three count off each other from 1, and just report the number without any other information.",
    role="user",
)

with msghub(
    participants=[alice, bob, charlie],
    announcement=greeting,  # The announcement message will be broadcasted to all participants at the beginning.
) as hub:
    # The first round of the conversation
    alice()
    bob()
    charlie()

    # We can manage the participants dynamically, e.g. delete an agent from the conversation.
    hub.delete(charlie)

    # Broadcast a message to all participants
    hub.broadcast(
        Msg(
            "user",
            "Charlie has left the conversation.",
            "user",
        ),
    )

    # The second round of the conversation
    alice()
    bob()
    charlie()
