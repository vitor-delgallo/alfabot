let isLoading = false;
        let loadingDots = 0;
        let loadingInterval;

        function toggleButton() {
            const question = document.getElementById('question').value;
            const sendButton = document.getElementById('send-button');
            sendButton.disabled = !question.trim();
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

            // Adiciona "Escrevendo..." para o AsimoBot
            const botDiv = document.createElement('div');
            botDiv.className = 'bot';
            botDiv.innerText = 'AsimoBot: Escrevendo';
            historyElement.appendChild(botDiv);

            // Alterna os "..." de Escrevendo
            isLoading = true;
            loadingInterval = setInterval(() => {
                loadingDots = (loadingDots + 1) % 4;
                botDiv.innerText = `AsimoBot: Escrevendo${'.'.repeat(loadingDots)}`;
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

                // Atualiza o texto do AsimoBot
                botDiv.innerText = `AsimoBot: ${data.history[data.history.length - 1][1]}`;

                // Limpa o campo de entrada
                document.getElementById('question').value = '';
                toggleButton();
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