# Importa bibliotecas de uso externo
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders import PyPDFLoader

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