// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    const sendButton = document.getElementById('send-button');
    const userInput = document.getElementById('user-input');
    const chatbox = document.getElementById('chatbox');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;

        appendMessage('user', message);
        userInput.value = '';

        fetch('/chatbot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'message': message })
        })
        .then(response => response.json())
        .then(data => {
            appendMessage('bot', data.message);
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('bot', "Sorry, I'm having trouble processing your request right now.");
        });
    }

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (sender === 'user') {
            messageElement.classList.add('user-message');
            messageElement.innerHTML = `<strong>You:</strong> ${message}`;
        } else {
            messageElement.classList.add('bot-message');
            const formattedMessage = message.replace(/\n/g, '<br>');
            messageElement.innerHTML = `<strong>Bot:</strong> ${formattedMessage}`;
        }
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
});
