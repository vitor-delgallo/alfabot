let isLoading = false;
let loadingDots = 0;
let loadingInterval;

function toggleButton() {
    const question = document.getElementById('question').value;
    const sendButton = document.getElementById('send-button');
    sendButton.disabled = !question.trim();
}

function scrollToBottom() {
    const historyElement = document.getElementById('chat-history');
    historyElement.scrollTop = historyElement.scrollHeight;
}

async function sendQuestion() {
    const question = document.getElementById('question').value;
    const historyElement = document.getElementById('chat-history');
    const sendButton = document.getElementById('send-button');

    if (!question.trim()) return;

    // Adiciona ao histórico o texto do usuário
    const userDiv = document.createElement('div');
    userDiv.className = 'user';
    userDiv.innerText = `Você: ${question}`;
    historyElement.appendChild(userDiv);

    // Adiciona "Escrevendo..." para o ALFABot
    const botDiv = document.createElement('div');
    botDiv.className = 'bot';
    botDiv.innerText = 'ALFABot: Escrevendo';
    historyElement.appendChild(botDiv);

    scrollToBottom();

    // Alterna os "..." de Escrevendo
    isLoading = true;
    loadingInterval = setInterval(() => {
        loadingDots = (loadingDots + 1) % 4;
        botDiv.innerText = `ALFABot: Escrevendo${'.'.repeat(loadingDots)}`;
    }, 500);

    // Desabilita o botão e altera o texto
    sendButton.disabled = true;
    sendButton.innerText = 'Carregando';
    let buttonDots = 0;
    const buttonInterval = setInterval(() => {
        buttonDots = (buttonDots + 1) % 4;
        sendButton.innerText = `Carregando${'.'.repeat(buttonDots)}`;
    }, 500);

    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        clearInterval(loadingInterval);
        clearInterval(buttonInterval);
        isLoading = false;

        if (data.error) {
            alert(data.error);
            return;
        }

        // Atualiza o texto do ALFABot
        botDiv.innerText = `ALFABot: ${data.history[data.history.length - 1][1]}`;

        // Limpa o campo de entrada
        document.getElementById('question').value = '';
        toggleButton();
        scrollToBottom();
    } catch (error) {
        console.error(error);
        alert("Erro ao se conectar ao servidor.");
    } finally {
        clearInterval(loadingInterval);
        clearInterval(buttonInterval);
        isLoading = false;
        sendButton.disabled = false;
        sendButton.innerText = 'Enviar';
    }
}

function exitChat() {
    const historyElement = document.getElementById('chat-history');
    const exitButton = document.getElementById('exit-button');
    const sendButton = document.getElementById('send-button');
    const startNewChatButton = document.getElementById('start-new-chat');

    const botDiv = document.createElement('div');
    botDiv.className = 'bot';
    botDiv.innerText = document.getElementById('default-message-exit').innerText;
    historyElement.appendChild(botDiv);

    sendButton.style.display = 'none';
    exitButton.style.display = 'none';
    startNewChatButton.style.display = 'flex';

    scrollToBottom();
}

async function startNewChat() {
    const startNewChatButton = document.getElementById('start-new-chat');
    const historyElement = document.getElementById('chat-history');
    const sendButton = document.getElementById('send-button');
    const exitButton = document.getElementById('exit-button');

    startNewChatButton.disabled = true;
    startNewChatButton.innerText = 'Carregando';

    let buttonDots = 0;
    const buttonInterval = setInterval(() => {
        buttonDots = (buttonDots + 1) % 4;
        startNewChatButton.innerText = `Carregando${'.'.repeat(buttonDots)}`;
    }, 500);

    try {
        const response = await fetch('http://127.0.0.1:5000/init', {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Erro ao iniciar novo chat');
        }

        clearInterval(buttonInterval);

        historyElement.innerHTML = document.getElementById('default-message-hello').innerHTML;
        sendButton.style.display = 'flex';
        exitButton.style.display = 'flex';
        startNewChatButton.style.display = 'none';

        document.getElementById('question').value = '';
        toggleButton();
        scrollToBottom();
    } catch (error) {
        console.error(error);
        alert(error.message);
    } finally {
        clearInterval(buttonInterval);
        startNewChatButton.disabled = false;
        startNewChatButton.innerText = 'Iniciar Novo Chat';
    }
}

startNewChat();