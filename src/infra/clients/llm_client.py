import os
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from src.config.settings import settings
from src.utils.logger import setup_logger
from openai import OpenAIError

logger = setup_logger()

class LLMClient:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            max_tokens=1000
        )
        self.retrieval = self._initialize_retrieval()
        self.prompt = self._initialize_prompt()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type(OpenAIError),
        before_sleep=lambda retry_state: logger.info(f"Retrying due to OpenAIError: attempt {retry_state.attempt_number}")
    )
    def _initialize_retrieval(self):
        """Inicializa o FAISS com cache."""
        loader = CSVLoader(file_path=settings.CSV_FILE_PATH)
        embeddings = OpenAIEmbeddings()
        if os.path.exists(settings.FAISS_INDEX_PATH):
            vector_store = FAISS.load_local(settings.FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        else:
            documents = loader.load()
            vector_store = FAISS.from_documents(documents, embeddings)
            vector_store.save_local(settings.FAISS_INDEX_PATH)
        return vector_store.as_retriever()

    @staticmethod
    def _initialize_prompt():
        """Inicializa o prompt do LangChain."""
        template = "Você é um atendente de IA, contexto:{context}, pergunta:{question}, histórico de conversas:{chat_history}"
        return ChatPromptTemplate.from_template(template)

    def generate_response(self, message: str, chat_history: str) -> str:
        """Gera uma resposta usando o LangChain."""
        try:
            chain = (
                {"context": self.retrieval, "question": RunnablePassthrough(), "chat_history": lambda _: chat_history}
                | self.prompt
                | self.llm
            )
            response = chain.invoke(message)
            return response.content
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua mensagem."