import flask
from src.application.usecases.proccess_message_usecase import ProcessMessageUseCase
from src.infra.http.evolution_api import EvolutionAPIClient
from src.utils.logger import setup_logger

logger = setup_logger()

def create_app(use_case: ProcessMessageUseCase, evolution_api: EvolutionAPIClient):
    app = flask.Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def webhook():
        """Endpoint para receber mensagens via webhook."""
        try:
            data = flask.request.json
            if not data or 'data' not in data or 'message' not in data['data']:
                logger.error("Estrutura de dados inválida recebida")
                return flask.jsonify({"error": "Estrutura de dados inválida"}), 400

            message = data['data']['message']['conversation']
            if not message.strip():
                logger.warning("Mensagem vazia recebida")
                return flask.jsonify({"error": "Mensagem vazia"}), 400

            instance = data['instance']
            instance_key = data['apikey']
            sender_number = data['data']['key']['remoteJid'].split("@")[0]

            response = use_case.execute(message, sender_number)
            evolution_api.send_message(response, instance, instance_key, sender_number)

            return flask.jsonify({"response": message})
        except KeyError as e:
            logger.error(f"Erro nos dados da requisição: {e}")
            return flask.jsonify({"error": f"Dados ausentes: {e}"}), 400
        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            return flask.jsonify({"error": "Erro interno do servidor"}), 500

    return app