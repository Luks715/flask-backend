document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', async function(event) {
        // 1. Impede o comportamento padrão de recarregar a página
        event.preventDefault();

        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const errorMsg = document.getElementById('errorMsg');
        const btnSubmit = document.getElementById('btnSubmit');

        // Limpa mensagem de erro anterior
        errorMsg.style.display = 'none';
        
        // Feedback visual de carregamento
        const originalBtnText = btnSubmit.innerText;
        btnSubmit.innerText = "Verificando...";
        btnSubmit.disabled = true;

        const payload = {
            username: usernameInput.value,
            password: passwordInput.value
        };

        try {
            // 2. Faz o POST para o endpoint
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            // 3. Verifica o status da resposta
            if (response.ok) {
                // Login com sucesso (200 OK)
                // Redireciona para a raiz
                window.location.href = '/'; 
            } else {
                // Erro (401, 404, etc)
                errorMsg.style.display = 'block';
                errorMsg.innerText = "Usuário ou senha incorretos.";
            }

        } catch (error) {
            console.error('Erro na requisição:', error);
            errorMsg.style.display = 'block';
            errorMsg.innerText = "Erro de conexão com o servidor.";
        } finally {
            // Restaura o botão
            btnSubmit.innerText = originalBtnText;
            btnSubmit.disabled = false;
        }
    });
});