# Importa bibliotecas próprias do sistema
import os
import sys

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


# Importa biblioteca para controle de dotenv
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()