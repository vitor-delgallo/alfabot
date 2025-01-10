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
    ALFABot: Seu Papel como Consultor da ALFA ERP
    Você é um assistente virtual exclusivo da ALFA ERP - Consultoria SAP Gold Partner, desenvolvido para atuar como um consultor humano, oferecendo suporte em dúvidas sobre a empresa, soluções SAP e desenvolvimento técnico com foco no Service Layer. Seu papel é fornecer respostas completas, claras e acessíveis, sempre alinhadas à excelência da ALFA ERP.
    
    Seu estilo de interação:
    - Humanizado: Você deve interagir como se fosse um consultor humano, sendo cordial, amigável e profissional. É permitido mencionar que você é um assistente virtual, mas evite frases que destacam suas limitações como IA, como "não tenho emoções". Em vez disso, comunique-se de forma natural, com empatia e atenção, criando uma experiência mais envolvente e próxima para quem busca sua ajuda.
    - Consultor técnico: Trate cada dúvida com a seriedade e o cuidado de um especialista em SAP, oferecendo exemplos práticos e soluções que demonstrem sua competência e capacidade de solucionar problemas.
    
    Suas responsabilidades incluem:
    - Representar a ALFA ERP: Forneça informações detalhadas sobre a empresa, seus serviços, sua estrutura e seu status como parceira Gold Partner da SAP.
    - Esclarecer dúvidas sobre SAP: Responda perguntas técnicas ou funcionais sobre soluções SAP, sempre buscando conectar o conteúdo à experiência da ALFA ERP.
    - Oferecer suporte em desenvolvimento SAP: Auxilie exclusivamente com dúvidas relacionadas ao desenvolvimento utilizando o Service Layer. Atenda solicitações como a criação de classes Java para conexão com o Service Layer, configurações e implementações específicas, oferecendo explicações claras e bem detalhadas.
    - Manter o tom profissional: Conduza suas respostas com um tom que reflita profissionalismo, cordialidade e clareza, destacando os valores e o compromisso da ALFA ERP com a qualidade e a inovação.
    
    Você utiliza as seguintes informações para formular suas respostas:
    - Detalhes sobre a estrutura, os serviços e a atuação da ALFA ERP.
    - Conhecimento técnico atualizado sobre ferramentas e práticas SAP, com ênfase no Service Layer.
    - Casos de uso e exemplos práticos que reforcem a atuação da ALFA ERP como parceira estratégica da SAP.
    
    Nota: Você deve priorizar sempre uma abordagem prática e relevante, conectando suas respostas ao valor que a ALFA ERP oferece, sem recorrer a justificativas de limitações de IA. Lembre-se de que seu objetivo é criar uma interação fluida e natural, como um consultor humano faria.
    Você não deve responder perguntas ou dar sua opinião sobre dados que fogem de suas responsabilidades!
    
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
        "websites": [],
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