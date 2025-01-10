from flask import Blueprint, render_template, request, jsonify
from utils.bot_logic import send_message, initialize_chatbot

bp = Blueprint('routes', __name__)

# Rota para servir o index.html
@bp.route('/')
def home():
    """
    Renderiza o arquivo index.html da pasta templates.
    """
    return render_template('index.html')

# Endpoint para enviar perguntas e receber respostas
@bp.route('/ask', methods=['POST'])
def ask():
    """
    Endpoint para receber perguntas e retornar respostas, mantendo o histórico.
    """
    # Recebe a pergunta em formato JSON
    data_json = request.get_json()
    question = data_json.get('question', '')

    # Retorno de erro se o prompt for vazio
    if not question:
        return jsonify({'error': 'Pergunta não fornecida'}), 400

    # Chama a função do script
    return jsonify(send_message(question))

# Endpoint para iniciar o bot
@bp.route('/init', methods=['POST'])
def init():
    """
    Endpoint para reiniciar o bot
    """

    # Chama a função do script
    initialize_chatbot()
    return jsonify({})
