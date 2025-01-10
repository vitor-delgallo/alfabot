# Importa bibliotecas próprias do sistema para checagem de requirements
#  antes da inicialização do sistema
import os
import subprocess
import sys

# Função para instalar as dependências automaticamente
def install_requirements():
    """
    Instala os pacotes listados no arquivo requirements.txt.
    Usa subprocess para chamar o pip e garantir que as dependências estejam presentes.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Instalar as dependências
install_requirements()

# Importa bibliotecas de uso externo
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# ===== FUNÇÕES AUXILIARES =====
def get_env_variable(key):
    """
    Obtém uma variável de ambiente.

    Args:
        key (str): Nome da variável de ambiente.

    Returns:
        str: Valor da variável de ambiente.

    Raises:
        SystemExit: Se a variável de ambiente não estiver definida.
    """
    value = os.getenv(key)
    if value is None:
        print(f"Erro: A variável de ambiente '{key}' não está definida.")
        sys.exit(1)  # Encerra o programa com código de erro
    return value

def load_website(url_site):
    """
    Carrega o conteúdo de um site e retorna o texto extraído.

    Args:
        url_site (str): URL do site a ser carregado.

    Returns:
        str: Conteúdo extraído do site.
    """
    loader = WebBaseLoader(url_site)
    ret = ''
    for doc in loader.load():
        ret += doc.page_content
    return ret

def load_pdf(path):
    """
    Carrega o conteúdo de um arquivo PDF e retorna o texto extraído.

    Args:
        path (str): Caminho do arquivo PDF.

    Returns:
        str: Conteúdo extraído do PDF.
    """
    loader = PyPDFLoader(path)
    ret = ''
    for doc in loader.load():
        ret += doc.page_content
    return ret

def load_youtube(url):
    """
    Carrega o conteúdo transcrito de um vídeo do YouTube.

    Args:
        url (str): URL do vídeo do YouTube.

    Returns:
        str: Transcrição do conteúdo do vídeo.
    """
    loader = YoutubeLoader.from_youtube_url(url, language=['pt'])
    ret = ''
    for doc in loader.load():
        ret += doc.page_content
    return ret

def load_documents_from_sources(sources):
    """
    Carrega documentos de várias fontes: websites, PDFs e vídeos do YouTube.

    Args:
        sources (dict): Dicionário contendo listas de URLs de websites, caminhos de PDFs e URLs de vídeos do YouTube.

    Returns:
        str: Conteúdo combinado de todas as fontes.
    """

    documents = ""

    # Load websites
    for url in sources.get("websites", []):
        documents += load_website(url)

    # Load PDFs
    for pdf_path in sources.get("pdfs", []):
        documents += load_pdf(pdf_path)

    # Load YouTube videos
    for video_url in sources.get("youtube", []):
        documents += load_youtube(video_url)

    return documents
# ===== FUNÇÕES AUXILIARES =====

# Configurar a API Key para o ChatGroq
os.environ['GROQ_API_KEY'] = get_env_variable("GROQ_API_KEY")
chat = ChatGroq(model='llama-3.1-70b-versatile')

def resposta_bot(mensagens, documento):
    """
    Gera uma resposta do bot com base nas mensagens fornecidas e nas informações do documento.

    Args:
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

# Inicializa o bot com uma mensagem de boas-vindas
print('Bem-vindo ao ALFABot')

# Fontes predefinidas para carregar documentos
predefined_sources = {
    "websites": [],
    "pdfs": [],
    "youtube": []
}

# Inicialização de variaveis importantes ao sistema
documents = load_documents_from_sources(predefined_sources)
mensagens = []

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
    resposta = resposta_bot(mensagens, documents)
    mensagens.append(('assistant', resposta))

    # Imprime a resposta do bot
    print(f'Bot: {resposta}')

# Mensagem de encerramento do bot
print('Muito obrigado por usar o ALFABot!')