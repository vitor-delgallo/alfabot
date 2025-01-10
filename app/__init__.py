# Importa bibliotecas próprias do sistema para checagem de requirements
#  antes da inicialização do sistema
import subprocess
import sys
import os

# Função para instalar as dependências automaticamente
def install_requirements():
    """
    Instala os pacotes listados no arquivo requirements.txt.
    Usa subprocess para chamar o pip e garantir que as dependências estejam presentes.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def create_app():
    """
    Cria e configura o app Flask.
    """
    from flask import Flask
    app = Flask(__name__, static_folder=os.path.abspath('templates/assets'), template_folder=os.path.abspath('templates'))

    # Importa e registra as rotas
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

# Instala as dependências
install_requirements()

# Definição de variáveis do OS do sistema
from utils.env_handler import get_env_variable
os.environ["USER_AGENT"] = get_env_variable("USER_AGENT")