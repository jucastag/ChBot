// Load the SDK asynchronously
async function iniciarPrompt() {
    const response = await fetch('/');
    const data = await response.json();
    console.log(data);
    document.querySelector('#chat-messages').textContent = data.prompt;
    console.log('Valor del prompt iniciado:', data.prompt);
}
// Variable para controlar la visibilidad del chatbot
var isChatbotVisible = false;
async function toggleChatbot() {
    // Cambiar el valor de la variable isChatbotVisible
    console.log('Valor de isChatbotVisible antes de cambiarlo', isChatbotVisible);
    isChatbotVisible = !isChatbotVisible;
    console.log('Valor de isChatbotVisible después de cambiarlo', isChatbotVisible);
    // Obtener el elemento #chat-container
    console.log('Buscando #chat-container');
    const chatContainer = document.querySelector('#chat-container');
    // Si isChatbotVisible es true, mostrar el chatbot
    if (isChatbotVisible) {
        chatContainer.style.display = 'block';
        //iniciarPrompt();
        //sendUserMessage();
        //console.log('Enviando solicitud a /iniciar-prompt');
    } else {
        chatContainer.style.display = 'none';
    }

};

// Verificar que se recibió el valor correcto
//console.log('Valor del prompt iniciado:', data.prompt);
const form = document.querySelector('form');
const promptInput = document.querySelector('#prompt');
const maxTokensInput = document.querySelector('#max_tokens');
const responseElement = document.querySelector('#response');
const spinnerElement = document.querySelector('.spinner');


// Función para enviar un mensaje
function sendMessage(event) {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    if (event.key === 'Enter' || event.target.id === 'send-button') {
        event.preventDefault();
        if (userInput.value.trim() !== '') {
            sendUserMessage();
        }
    }
    sendButton.disabled = userInput.value.trim() === '';
}
async function sendUserMessage() {
    var userInput = document.getElementById('user-input');
    var chatMessages = document.getElementById('chat-messages');
    console.log('User input is', userInput.value);
    var userMessage = document.createElement('div');
    userMessage.className = 'message user-message';
    userMessage.innerHTML = userInput.value + '<span class="message-time">' + getTime() + '</span>';
    chatMessages.appendChild(userMessage);

    // Obtener la respuesta del bot utilizando una solicitud fetch
    const prompt = userInput.value;
    const response = await fetch(`/openai?pregunta=` + prompt);
    console.log('Enviando solicitud a /openai?pregunta=' + prompt);
    console.log('Respuesta de la solicitud', response);
    const botResponse = await response.text();

    console.log('Bot response is', botResponse);

    var botMessage = document.createElement('div');
    botMessage.className = 'message bot-message';
    botMessage.innerHTML = botResponse + '<span class="message-time">' + getTime() + '</span>';
    chatMessages.appendChild(botMessage);

    userInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
// Crear un objeto AbortController
const abortController = new AbortController();
// Realizar una solicitud HTTP asíncrona utilizando fetch()
fetch('/cerrar-conexion', {
    signal: abortController.signal
})
    .then(response => {
        // Manejar la respuesta de la solicitud
    })
    .catch(error => {
        // Manejar el error de la solicitud
    });
// Función para cerrar el chatbot
function closeChatbot() {
    var chatContainer = document.getElementById('chat-container');
    chatContainer.style.display = 'none';
    isChatbotVisible = false;
    // Cerrar la conexión API
    abortController.abort();
    //chatbotConfig.xhr.abort();
    console.log("Cerrando API Openai")
    // Limpiar el contenido de userMessage
    var userMessage = document.querySelector('.chat-messages');
    if (userMessage) {
        userMessage.textContent = '';
    }
}
function getTime() {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var time;

    if (hours >= 0 && hours < 12) {
        var ampm = 'am';
        hours = hours ? hours : 12;
        minutes = minutes < 10 ? '0' + minutes : minutes;
        time = hours + ':' + minutes + ' ' + ampm;
    } else {
        hours = hours < 10 ? '0' + hours : hours;
        minutes = minutes < 10 ? '0' + minutes : minutes;
        time = hours + ':' + minutes;
    }

    return time;
}