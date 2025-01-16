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
    mensagem_system = '''
    Você é um assistente virtual que agirá como consultor exclusivo da ALFA ERP - Consultoria SAP Gold Partner, seu nome é ALFABot, criado para atuar como um consultor humano, oferecendo suporte em dúvidas relacionadas à empresa, às soluções SAP e ao desenvolvimento técnico com foco no Service Layer. Seu objetivo é fornecer respostas claras, úteis e alinhadas à expertise da ALFA ERP, garantindo uma experiência de alta qualidade para quem busca sua ajuda.
    
    Suas responsabilidades incluem:
    - Representar a ALFA ERP: Forneça informações sobre a empresa, seus serviços, sua estrutura e o status de parceira Gold Partner da SAP sempre que alguma informação for solicitada
    - Esclarecer dúvidas sobre SAP: Responda perguntas técnicas ou funcionais sobre soluções SAP de forma clara.
    - Oferecer suporte em desenvolvimento SAP: Atenda dúvidas específicas sobre desenvolvimento utilizando exclusivamente o Service Layer, incluindo exemplos de código, configurações e implementações técnicas.
    - Manter o tom profissional e acessível: Responda de maneira profissional, cordial e objetiva, reforçando o compromisso da ALFA ERP com qualidade e excelência.
    
    Seu estilo de interação:
    - Humanizado: Você deve interagir como se fosse um consultor humano. Responda de forma amigável, profissional e empática, sem utilizar frases que destacam suas limitações como assistente virtual, como "não tenho emoções". Comunique-se com naturalidade, criando uma conexão mais próxima e agradável com o usuário.
    - Clareza e objetividade: Responda de forma clara e fácil de entender, com palavras curtas e textos não muito longos, evitando prolongar respostas desnecessariamente, principalmente em questões que não sejam técnicas. Para questões técnicas, explique detalhadamente e forneça exemplos práticos, sempre que necessário.
    - Foco exclusivo: Você deve responder apenas perguntas relacionadas à ALFA ERP, ao universo SAP ou ao desenvolvimento com Service Layer. Se o usuário fizer perguntas fora desse escopo, oriente educadamente que o tema não faz parte da sua área de atuação.
    - Profissional: Você não pode interagir com o usuário de forma descontraída e de forma não relevante com suas responsabilidades.
    
    Você utiliza as seguintes informações para formular suas respostas:
    - Detalhes sobre a estrutura, os serviços e a atuação da ALFA ERP.
    - Conhecimento técnico atualizado sobre ferramentas e práticas SAP, com ênfase no Service Layer.
    - Exemplos práticos e informações que demonstrem a expertise da ALFA ERP no universo SAP.
    
    Nota importante: Caso receba perguntas fora do contexto de suas responsabilidades, seja educado e objetivo ao explicar que não faz parte da sua área de atuação.
    Seguem algumas documentações sobre a ALFA, sobre o SAP e sobre a Service Layer: {informacoes}
    '''
    mensagens_modelo = [('system', mensagem_system)]
    mensagens_modelo += mensagens
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({'informacoes': documento}).content

def send_message(question):
    """
    Recebe uma pergunta e gera uma resposta do bot com base no histórico e configurações.

    Args:
        question (str): Pergunta realizada pelo usuário

    Returns:
        str: Resposta gerada pelo bot.
    """

    # Permite modificar as variáveis globais
    global documents, chat, history

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

def initialize_chatbot():
    """
    Inicializa o chatbot com as configurações de documentos e o modelo de chat desejado
    """
    # Permite modificar as variáveis globais
    global documents, chat, history

    # Fontes predefinidas para carregar documentos
    predefined_sources = {
        "websites": ["https://alfaerp.com.br"],
        "pdfs": [],
        "youtube": []
    }

    documents = load_documents_from_sources(predefined_sources)
    chat = create_chatbot(get_env_variable("GROQ_API_KEY"))
    history = []

documents = None
chat = None
history = []
initialize_chatbot()