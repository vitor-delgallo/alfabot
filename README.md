# Projeto: ALFA Chatbot

Este projeto implementa um chatbot utilizando Flask e o modelo `ChatGroq`, projetado para responder a perguntas relacionadas à empresa ALFA, SAP e Service Layer.

---

## **Pré-requisitos**

Antes de começar, certifique-se de que você possui:
- **Python 3.13.1** instalado (veja as instruções abaixo para configuração com `pyenv`).
- O gerenciador de pacotes `pip` instalado.
- Acesso ao repositório e permissões para clonar o projeto.

---

## **Configuração do Ambiente**

### 1. Instalar o Python com `pyenv`

1. Instale o Python 3.13.1 usando o comando:
   ```bash
   pyenv install 3.13.1
   ```

2. Configure o ambiente local do projeto:
   ```bash
   pyenv local 3.13.1
   ```

3. Atualize o `pip`:
   ```bash
   python -m pip install --upgrade pip
   ```

### 2. Clone o Repositório

Execute o seguinte comando no terminal para clonar o repositório do projeto:
```bash
cd <diretorio_de_projetos>
git clone https://github.com/vitorgd16/alfabot.git
```

---

### 3. Configure as Variáveis de Ambiente

Crie um arquivo `.env` no diretório raiz do projeto e configure-o conforme o arquivo `.env.example` incluído no repositório.

---

### 4. Instale as Dependências
Instale as dependências com o comando:
   ```bash
   pip install -r requirements.txt
   ```

---

### 5. Execute o Projeto

Depois de configurar tudo, você pode rodar o projeto com o seguinte comando:
```bash
python main.py
```

---

## **Estrutura do Projeto**

```plaintext
.
├── app/                       # Pasta de configurações do APP
│   ├── __init__.py            # Cria a instância do APP
│   ├── routes.py              # Define todas as rotas do sistema
├── templates/                 # Localização dos templates do projeto
│   ├── assets/                # Pasta de dados estáticos do template
│   │   ├── chat.js            # Lógica JS para fazer a ligação com o bot
│   │   ├── styles.css         # Folha de estilo do projeto
│   ├── index.html             # HTML template do projeto (Visual do sistema)
├── utils/                     # Todos os Helpers do sistema
│   ├── bot_logic.py           # Helpers que lidam com a lógica do bot
│   ├── document_loaders.py    # Helpers para dar load em informações para a IA
│   ├── env_handler.py         # Helpers que lidam com o arquivo ENV
├── .env                       # Variáveis de ambiente (não versionado)
├── .env.example               # Exemplo para variáveis de ambiente do projeto
├── .gitignore                 # Listagem de arquivos ignorados no GIT
├── instructions.txt           # Arquivo de instruções do desenvolvedor
├── main.py                    # Executável principal do projeto
├── README.md                  # Documentação do projeto
└── requirements.txt           # Dependências do pip
└── requirements_dev.txt       # Dependências do pip resumido para DEV's
```

---

## **Suporte**

Caso tenha dúvidas ou problemas, entre em contato com o administrador do repositório.
