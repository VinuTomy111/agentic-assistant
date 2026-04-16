from typing import List, Dict, Any

class ShortTermMemory:
    """
    Manages the short-term context of the current conversation/session.
    Stores messages in a format that can be easily fed to the LLM.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def add_message(self, role: str, content: str):
        """
        Adds a single message to the conversation history.
        Role can be 'system', 'user', 'assistant', or 'tool'.
        """
        self.history.append({"role": role, "content": content})
        
    def add_tool_message(self, tool_name: str, content: str):
         """
         Adds a message specifically for tool results.
         """
         self.history.append({"role": "tool", "name": tool_name, "content": content})

    def get_history(self) -> List[Dict[str, Any]]:
        """
        Returns the entire short-term memory history.
        """
        return self.history

    def get_context_string(self) -> str:
        """
        Returns the history formatted as a single readable string.
        """
        result = []
        for msg in self.history:
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")
            result.append(f"[{role}]: {content}")
        return "\n".join(result)

    def clear(self):
        """
        Clears the short-term memory.
        """
        self.history = []
