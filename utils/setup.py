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

# Instala as dependências
install_requirements()

# Importa biblioteca para controle de dotenv
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()