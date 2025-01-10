# Importa bibliotecas utilitárias para o funcionamento da aplicação
from utils.setup import get_env_variable
from utils.document_loaders import load_documents_from_sources
from utils.bot_logic import create_chatbot, get_chatbot_response

# Fontes predefinidas para carregar documentos
predefined_sources = {
    "websites": [],
    "pdfs": [],
    "youtube": []
}

# Inicialização de variaveis importantes ao sistema
documents = load_documents_from_sources(predefined_sources)
chat = create_chatbot(get_env_variable("GROQ_API_KEY"))
mensagens = []

# Inicializa o bot com uma mensagem de boas-vindas
print("Bem-vindo ao ALFABot")

# Loop principal do chatbot
while True:
    #Obtêm o prompt do usuário
    pergunta = input('Usuario: ')

    # Encerra o loop se o prompt for igual a mensagem para encerrar o sistema
    if pergunta.lower() == 'x':
        break

    # Envia o prompt ao bot, junto com as mensagens anteriores e os
    #  documentos para obtenção da resposta
    mensagens.append(('user', pergunta))
    resposta = get_chatbot_response(chat, mensagens, documents)
    mensagens.append(('assistant', resposta))

    # Imprime a resposta do bot
    print(f"Bot: {resposta}")

# Mensagem de encerramento do bot
print("Muito obrigado por usar o ALFABot!")