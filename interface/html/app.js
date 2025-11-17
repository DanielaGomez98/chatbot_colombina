// ========== Configuration ==========
const API_BASE_URL = 'https://chatbotcolombina-production.up.railway.app';
const MAX_MESSAGE_LENGTH = 2000;
const TYPING_DELAY = 500; // ms

// ========== State Management ==========
let sessionId = generateSessionId();
let isProcessing = false;
let modelSettings = {
    temperature: 0.0,
    top_p: 0.9,
    max_tokens: null
};

// ========== DOM Elements ==========
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const charCount = document.getElementById('charCount');
const sessionIdDisplay = document.getElementById('sessionId');
const newChatBtn = document.getElementById('newChatBtn');
const typingIndicator = document.getElementById('typingIndicator');
const suggestionBtns = document.querySelectorAll('.suggestion-btn');
const errorToast = document.getElementById('errorToast');
const toastMessage = document.getElementById('toastMessage');
const toastClose = document.getElementById('toastClose');

// Settings elements
const settingsBtn = document.getElementById('settingsBtn');
const settingsPanel = document.getElementById('settingsPanel');
const closeSettings = document.getElementById('closeSettings');
const temperatureSlider = document.getElementById('temperatureSlider');
const temperatureValue = document.getElementById('temperatureValue');
const topPSlider = document.getElementById('topPSlider');
const topPValue = document.getElementById('topPValue');
const maxTokensInput = document.getElementById('maxTokensInput');
const maxTokensValue = document.getElementById('maxTokensValue');
const resetSettings = document.getElementById('resetSettings');

// ========== Utility Functions ==========
function generateSessionId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString('es-CO', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatBotMessage(text) {
    // Convert markdown-style formatting to HTML
    let formatted = escapeHtml(text);
    
    // Bold: **text** or __text__
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    formatted = formatted.replace(/__(.+?)__/g, '<strong>$1</strong>');
    
    // Italic: *text* or _text_
    formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
    formatted = formatted.replace(/_(.+?)_/g, '<em>$1</em>');
    
    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    // Lists (simple implementation)
    formatted = formatted.replace(/^- (.+)$/gm, '• $1');
    
    return formatted;
}

function scrollToBottom() {
    chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: 'smooth'
    });
}

// ========== UI Functions ==========
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = `
        <div class="avatar ${isUser ? 'user-avatar' : 'bot-avatar'}">
            ${isUser ? '👤' : '🤖'}
        </div>
    `;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const formattedContent = isUser ? escapeHtml(content) : formatBotMessage(content);
    
    contentDiv.innerHTML = `
        <div class="message-bubble">
            <p>${formattedContent}</p>
        </div>
        <div class="message-time">${formatTime()}</div>
    `;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    typingIndicator.classList.add('active');
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.classList.remove('active');
}

function showError(message) {
    toastMessage.textContent = message;
    errorToast.classList.add('show');
    
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorToast.classList.remove('show');
}

function updateCharCount() {
    const length = messageInput.value.length;
    charCount.textContent = `${length}/${MAX_MESSAGE_LENGTH}`;
    
    if (length > MAX_MESSAGE_LENGTH) {
        charCount.style.color = 'var(--error-color)';
    } else {
        charCount.style.color = 'var(--text-secondary)';
    }
}

function setProcessingState(processing) {
    isProcessing = processing;
    sendBtn.disabled = processing;
    messageInput.disabled = processing;
    
    suggestionBtns.forEach(btn => {
        btn.disabled = processing;
    });
}

function clearWelcomeMessage() {
    const welcomeMessage = chatMessages.querySelector('.bot-message');
    if (welcomeMessage && welcomeMessage.textContent.includes('Bienvenido')) {
        welcomeMessage.remove();
    }
}

// ========== API Functions ==========
async function sendMessage(message) {
    try {
        const requestBody = {
            message: message,
            session_id: sessionId,
            temperature: modelSettings.temperature,
            top_p: modelSettings.top_p
        };
        
        // Only include max_tokens if it's set
        if (modelSettings.max_tokens !== null) {
            requestBody.max_tokens = modelSettings.max_tokens;
        }
        
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
}

// ========== Event Handlers ==========
async function handleSubmit(e) {
    e.preventDefault();
    
    const message = messageInput.value.trim();
    
    if (!message || isProcessing) {
        return;
    }
    
    if (message.length > MAX_MESSAGE_LENGTH) {
        showError(`El mensaje es demasiado largo. Máximo ${MAX_MESSAGE_LENGTH} caracteres.`);
        return;
    }
    
    // Clear welcome message on first user interaction
    clearWelcomeMessage();
    
    // Add user message to chat
    addMessage(message, true);
    
    // Clear input
    messageInput.value = '';
    updateCharCount();
    
    // Auto-resize textarea
    messageInput.style.height = 'auto';
    
    // Set processing state
    setProcessingState(true);
    showTypingIndicator();
    
    try {
        // Send message to API
        const response = await sendMessage(message);
        
        // Simulate typing delay for better UX
        await new Promise(resolve => setTimeout(resolve, TYPING_DELAY));
        
        // Add bot response
        hideTypingIndicator();
        addMessage(response, false);
        
    } catch (error) {
        hideTypingIndicator();
        showError('Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.');
        
        // Add error message to chat
        addMessage(
            'Disculpa, tuve un problema al procesar tu solicitud. ¿Podrías intentarlo de nuevo?',
            false
        );
    } finally {
        setProcessingState(false);
        messageInput.focus();
    }
}

function handleSuggestionClick(e) {
    const question = e.currentTarget.dataset.question;
    if (question && !isProcessing) {
        messageInput.value = question;
        updateCharCount();
        handleSubmit(new Event('submit'));
    }
}

function handleNewChat() {
    if (isProcessing) {
        return;
    }
    
    // Confirm with user
    const confirmNew = confirm('¿Estás seguro de que deseas iniciar una nueva conversación? Se perderá el historial actual.');
    
    if (confirmNew) {
        // Generate new session ID
        sessionId = generateSessionId();
        sessionIdDisplay.textContent = sessionId.substring(0, 8);
        
        // Clear chat messages
        chatMessages.innerHTML = `
            <div class="message bot-message">
                <div class="message-avatar">
                    <div class="avatar bot-avatar">🤖</div>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <p>¡Bienvenido al Chatbot de Colombina! 🍭</p>
                        <p>Soy tu asistente virtual y estoy aquí para ayudarte con información sobre nuestros productos, la empresa, sostenibilidad, y mucho más.</p>
                        <p>¿En qué puedo ayudarte hoy?</p>
                    </div>
                    <div class="message-time">${formatTime()}</div>
                </div>
            </div>
        `;
        
        // Clear input
        messageInput.value = '';
        updateCharCount();
        
        // Focus input
        messageInput.focus();
    }
}

function handleInputResize() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

function toggleSettings() {
    const isVisible = settingsPanel.style.display !== 'none';
    settingsPanel.style.display = isVisible ? 'none' : 'block';
}

function updateTemperature() {
    const value = parseFloat(temperatureSlider.value);
    modelSettings.temperature = value;
    temperatureValue.textContent = value.toFixed(1);
}

function updateTopP() {
    const value = parseFloat(topPSlider.value);
    modelSettings.top_p = value;
    topPValue.textContent = value.toFixed(2);
}

function updateMaxTokens() {
    const value = maxTokensInput.value;
    if (value === '' || value === null) {
        modelSettings.max_tokens = null;
        maxTokensValue.textContent = 'Auto';
    } else {
        modelSettings.max_tokens = parseInt(value);
        maxTokensValue.textContent = value;
    }
}

function resetModelSettings() {
    modelSettings = {
        temperature: 0.0,
        top_p: 0.9,
        max_tokens: null
    };
    
    temperatureSlider.value = 0;
    temperatureValue.textContent = '0.0';
    
    topPSlider.value = 0.9;
    topPValue.textContent = '0.9';
    
    maxTokensInput.value = '';
    maxTokensValue.textContent = 'Auto';
    
    showError('Configuración restaurada a valores por defecto');
}

// ========== Initialization ==========
function initializeChat() {
    // Display session ID (first 8 characters)
    sessionIdDisplay.textContent = sessionId.substring(0, 8);
    
    // Event Listeners
    chatForm.addEventListener('submit', handleSubmit);
    messageInput.addEventListener('input', () => {
        updateCharCount();
        handleInputResize();
    });
    
    // Prevent Enter from creating new line (submit instead)
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    });
    
    suggestionBtns.forEach(btn => {
        btn.addEventListener('click', handleSuggestionClick);
    });
    
    newChatBtn.addEventListener('click', handleNewChat);
    toastClose.addEventListener('click', hideError);
    
    // Settings event listeners
    settingsBtn.addEventListener('click', toggleSettings);
    closeSettings.addEventListener('click', toggleSettings);
    temperatureSlider.addEventListener('input', updateTemperature);
    topPSlider.addEventListener('input', updateTopP);
    maxTokensInput.addEventListener('input', updateMaxTokens);
    resetSettings.addEventListener('click', resetModelSettings);
    
    // Focus input on load
    messageInput.focus();
    
    // Initialize character count
    updateCharCount();
    
    console.log('🤖 Chatbot inicializado correctamente');
    console.log(`📋 Session ID: ${sessionId}`);
}

// ========== Health Check ==========
async function checkApiHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ API conectada correctamente');
        } else {
            throw new Error('API no disponible');
        }
    } catch (error) {
        console.warn('⚠️ No se pudo conectar con la API:', error.message);
        showError('Advertencia: No se pudo conectar con el servidor.');
    }
}

// ========== Start Application ==========
document.addEventListener('DOMContentLoaded', () => {
    initializeChat();
    checkApiHealth();
});

// ========== Export for Testing ==========
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        generateSessionId,
        formatTime,
        escapeHtml,
        formatBotMessage,
        sendMessage
    };
}
