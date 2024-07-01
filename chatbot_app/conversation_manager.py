# conversation_manager.py
import weave

class ConversationManager:
    def __init__(self):
        self.messages = []

    @weave.op()
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    @weave.op()
    def add_tool_result(self, tool_use_id, content):
        self.messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_id,
                    "content": str(content),
                }
            ],
        })

    @weave.op()
    def get_messages(self):
        return self.messages