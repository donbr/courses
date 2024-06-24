# conversation_manager.py
class ConversationManager:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

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

    def get_messages(self):
        return self.messages