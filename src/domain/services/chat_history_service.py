from src.domain.entities.chat_history import ChatHistory

class ChatHistoryService:
    def __init__(self, storage):
        self.storage = storage

    def get_history(self, sender_number: str) -> ChatHistory:
        """Recupera o histórico de conversa do armazenamento."""
        history_data = self.storage.get(sender_number)
        return ChatHistory(history_data)

    def update_history(self, sender_number: str, user_message: str, bot_response: str) -> ChatHistory:
        """Atualiza o histórico de conversa no armazenamento."""
        history = self.get_history(sender_number)
        history.add_entry(user_message, bot_response)
        self.storage.save(sender_number, history.to_dict())
        return history