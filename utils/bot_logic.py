# Importa bibliotecas necessárias para o funcionamento do bot
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from utils.document_loaders import load_documents_from_sources
from utils.env_handler import get_env_variable

def create_chatbot(api_key, model="llama-3.1-70b-versatile"):
    """
    Configura o chatbot com a chave da API e o modelo.
    """
    os.environ['GROQ_API_KEY'] = api_key
    return ChatGroq(model=model)

def get_chatbot_response(chat, mensagens, documento):
    """
    Gera uma resposta do bot com base nas mensagens fornecidas e nas informações do documento.

    Args:
        chat (ChatGroq): Referência do ChatGroq com o modelo escolhido
        mensagens (list): Lista de mensagens no formato (role, message).
        documento (str): Informações adicionais para o contexto.

    Returns:
        str: Resposta gerada pelo bot.
    """
    mensagem_system = '''Você é um assistente amigável chamado Asimo.
    Você utiliza as seguintes informações para formular as suas respostas: {informacoes}'''
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content

# Fontes predefinidas para carregar documentos
predefined_sources = {
    "websites": [],
    "pdfs": [],
    "youtube": []
}

# Inicialização de variaveis importantes ao sistema
documents = load_documents_from_sources(predefined_sources)
chat = create_chatbot(get_env_variable("GROQ_API_KEY"))
history = []

def send_message(question):
    """
    Recebe uma pergunta e gera uma resposta do bot com base no histórico e configurações.

    Args:
        question (str): Pergunta realizada pelo usuário

    Returns:
        str: Resposta gerada pelo bot.
    """

    # Retorno vazio se a question for vazia
    if not question:
        return {'answer': '', 'history': history}

    # Adiciona a nova pergunta ao histórico
    history.append(('user', question))

    # Processa a pergunta com o chatbot usando o histórico
    response = get_chatbot_response(chat, history, documents)

    # Adiciona a resposta ao histórico
    history.append(('assistant', response))

    # Retorna a resposta do bot
    return {'answer': response, 'history': history}