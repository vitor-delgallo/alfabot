async function sendQuestion() {
    const question = document.getElementById('question').value;
    const historyElement = document.getElementById('chat-history');

    if (!question.trim()) {
        alert("Por favor, insira uma pergunta!");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();
        if (data.error) {
            alert(data.error);
            return;
        }

        // Atualiza o histórico no frontend
        const history = data.history;
        historyElement.innerHTML = ""; // Limpa o histórico para re-renderizar
        history.forEach(([role, message]) => {
            const div = document.createElement('div');
            div.innerText = `${role === 'user' ? 'Você' : 'AsimoBot'}: ${message}`;
            historyElement.appendChild(div);
        });

        // Limpa o campo de entrada
        document.getElementById('question').value = '';
    } catch (error) {
        console.error(error);
        alert("Erro ao se conectar ao servidor.");
    }
}