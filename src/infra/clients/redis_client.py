import json
from typing import List, Dict
import redis
from redis import RedisError
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger()

class RedisStorage:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True,
            connection_pool=redis.ConnectionPool()
        )

    def get(self, sender_number: str) -> List[Dict[str, str]]:
        """Recupera o histórico de conversa do Redis."""
        history_key = f"chat_history:{sender_number}"
        try:
            history = self.client.get(history_key)
            if not history:
                return []
            return json.loads(history)
        except RedisError as e:
            logger.error(f"Erro ao acessar o Redis: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar histórico: {e}")
            return []

    def save(self, sender_number: str, history: List[Dict[str, str]]):
        """Salva o histórico de conversa no Redis."""
        history_key = f"chat_history:{sender_number}"
        try:
            self.client.set(history_key, json.dumps(history), ex=settings.CONTEXT_EXPIRY_SECONDS)
        except RedisError as e:
            logger.error(f"Erro ao atualizar o Redis: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao codificar histórico: {e}")