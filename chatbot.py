from openai import OpenAI
from dotenv import load_dotenv
from utils.evolutionAPI import EvolutionAPI
import flask
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

e = EvolutionAPI()
app = flask.Flask(__name__)
load_dotenv()

client = OpenAI()

loader = CSVLoader(file_path='Q&A.csv')	
documents = loader.load()
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(documents, embeddings)
retrieval = vector_store.as_retriever()

llm = ChatOpenAI()

template = "Você é um atendente de IA, contexto:{context}, pergunta:{question}"
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retrieval, "question": RunnablePassthrough()}
    | prompt
    | llm
)


def get_chat_response(message):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return completion.choices[0].message.content

@app.route("/webhook", methods=["POST"])
def webhook():
    data = flask.request.json
    message = data['data']['message']['conversation']
    instance = data['instance']
    instance_key = data['apikey']
    sender_number = data['data']['key']['remoteJid'].split("@")[0]
    # response = get_chat_response(message)
    response = chain.invoke(message)
    e.enviar_mensagem(response.content, instance, instance_key, sender_number)
    return flask.jsonify({"response": message})

# Remova o bloco de execução principal
if __name__ == "__main__":
    app.run(port=5000)