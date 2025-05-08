from src.domain.services.chat_history_service import ChatHistoryService
from src.infra.clients.llm_client import LLMClient
from src.utils.logger import setup_logger

logger = setup_logger()

class ProcessMessageUseCase:
    def __init__(self, chat_history_service: ChatHistoryService, llm_client: LLMClient):
        self.chat_history_service = chat_history_service
        self.llm_client = llm_client

    def execute(self, message: str, sender_number: str) -> str:
        """Processa uma mensagem e retorna a resposta."""
        try:
            history = self.chat_history_service.get_history(sender_number)
            formatted_history = history.format()
            response = self.llm_client.generate_response(message, formatted_history)
            self.chat_history_service.update_history(sender_number, message, response)
            return response
        except Exception as e:
            logger.error(f"Erro no caso de uso ProcessMessage: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."