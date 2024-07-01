# llm_interface.py
import os
import anthropic
import weave
from config import MODEL_NAME

weave.init("anthropic-tools")
client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))

@weave.op()
def get_llm_response(messages, system_prompt, tools):
    return client.messages.create(
        model=MODEL_NAME,
        system=system_prompt,
        max_tokens=1000,
        tools=tools,
        messages=messages
    )