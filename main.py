from src.config.settings import settings
from src.utils.logger import setup_logger
from src.infra.clients.redis_client import RedisStorage
from src.infra.clients.llm_client import LLMClient
from src.infra.http.evolution_api import EvolutionAPIClient
from src.domain.services.chat_history_service import ChatHistoryService
from src.application.usecases.proccess_message_usecase import ProcessMessageUseCase
from src.presentation.flask_app import create_app

logger = setup_logger()

def main():
    redis_storage = RedisStorage()
    llm_client = LLMClient()
    evolution_api = EvolutionAPIClient()
    chat_history_service = ChatHistoryService(redis_storage)
    process_message_use_case = ProcessMessageUseCase(chat_history_service, llm_client)

    app = create_app(process_message_use_case, evolution_api)
    logger.info(f"Iniciando servidor na porta {settings.FLASK_PORT}")
    app.run(port=settings.FLASK_PORT, debug=False)

if __name__ == "__main__":
    main()