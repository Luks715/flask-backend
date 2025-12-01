document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');

    registerForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm_password');
        const errorMsg = document.getElementById('errorMsg');
        const btnSubmit = document.getElementById('btnSubmit');

        // Limpa erros anteriores
        errorMsg.style.display = 'none';
        
        // --- VALIDAÇÃO DE SENHA ---
        if (passwordInput.value !== confirmPasswordInput.value) {
            errorMsg.innerText = "Senhas não conferem, tente novamente.";
            errorMsg.style.display = 'block';
            // Destaca visualmente o campo com erro (opcional, mas recomendado)
            confirmPasswordInput.value = ""; 
            confirmPasswordInput.focus();
            return; // Interrompe a função aqui, não envia para o servidor
        }
        // ---------------------------

        const originalBtnText = btnSubmit.innerText;
        btnSubmit.innerText = "Criando conta...";
        btnSubmit.disabled = true;

        const payload = {
            username: usernameInput.value,
            password: passwordInput.value
        };

        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                // Sucesso! Redireciona para o login com um parâmetro de URL
                window.location.href = '/auth/login?registered=true'; 
            } else {
                // Tenta pegar a mensagem de erro do JSON, se houver
                const data = await response.json();
                errorMsg.innerText = data.message || "Erro ao criar usuário.";
                errorMsg.style.display = 'block';
            }

        } catch (error) {
            console.error('Erro:', error);
            errorMsg.innerText = "Erro de conexão.";
            errorMsg.style.display = 'block';
        } finally {
            btnSubmit.innerText = originalBtnText;
            btnSubmit.disabled = false;
        }
    });
});