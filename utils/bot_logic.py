# Importa bibliotecas necessárias para o funcionamento do bot
import os
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

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