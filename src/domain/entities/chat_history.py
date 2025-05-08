from typing import List, Dict

class ChatHistory:
    def __init__(self, entries: List[Dict[str, str]] = None):
        self.entries = entries or []

    def add_entry(self, user_message: str, bot_response: str):
        """Adiciona uma nova interação ao histórico."""
        self.entries.append({"user": user_message, "assistant": bot_response})
        if len(self.entries) > 5:
            self.entries = self.entries[-5:]

    def format(self) -> str:
        """Formata o histórico para uso no prompt."""
        if not self.entries:
            return "Sem histórico anterior."
        formatted = ""
        for entry in self.entries:
            formatted += f"Usuário: {entry['user']}\n"
            formatted += f"Assistente: {entry['assistant']}\n\n"
        return formatted

    def to_dict(self) -> List[Dict[str, str]]:
        """Converte o histórico para um dicionário."""
        return self.entries