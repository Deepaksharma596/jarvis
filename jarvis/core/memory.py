"""
memory.py - Conversation History & Short-Term Entity Memory for JARVIS
"""
from typing import List, Dict, Any, Optional

class ConversationMemory:
    """Maintains recent conversation history and tracks context entities (e.g. 'it', 'the first result', last recipient)."""

    def __init__(self, max_turns: int = 15):
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []
        self.last_entities: Dict[str, Any] = {
            "last_contact": None,
            "last_app": None,
            "last_file": None,
            "last_search_results": [],
            "last_tool_output": None
        }

    def add_user_message(self, text: str):
        """Append user input."""
        self.history.append({"role": "user", "content": text})
        self._trim()

    def add_assistant_message(self, text: str):
        """Append assistant response."""
        self.history.append({"role": "assistant", "content": text})
        self._trim()

    def set_last_contact(self, contact_name: str):
        self.last_entities["last_contact"] = contact_name

    def set_last_app(self, app_name: str):
        self.last_entities["last_app"] = app_name

    def set_last_file(self, file_path: str):
        self.last_entities["last_file"] = file_path

    def set_search_results(self, results: list):
        self.last_entities["last_search_results"] = results

    def set_last_tool_output(self, output: str):
        self.last_entities["last_tool_output"] = output

    def resolve_reference(self, text: str) -> str:
        """Replace pronouns and relative references based on memory."""
        lower = text.lower()
        if "the first result" in lower or "first link" in lower or "first video" in lower:
            if self.last_entities["last_search_results"]:
                first = self.last_entities["last_search_results"][0]
                return text.replace("the first result", str(first)).replace("first link", str(first)).replace("first video", str(first))
        
        if "open it" in lower or "read it" in lower or "summarize it" in lower:
            if self.last_entities["last_file"]:
                return text.replace("it", self.last_entities["last_file"])
        
        return text

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def get_formatted_history(self) -> List[Dict[str, str]]:
        return self.history[-self.max_turns:]

    def _trim(self):
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def clear(self):
        self.history.clear()
        self.last_entities = {
            "last_contact": None,
            "last_app": None,
            "last_file": None,
            "last_search_results": [],
            "last_tool_output": None
        }
