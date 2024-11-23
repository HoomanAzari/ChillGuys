const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessage = document.querySelector("#send-message");

const userData = {
    message: null
}

// Create a message element with dynamic classes and return it
const createMessageElement = (content, classes) => {
    const div = document.createElement("div");
    div.classList.add("message", classes);
    div.innerHTML = content;
    return div;
}

// Handles outgoing user messages
const handleOutgoingMessage = (e) => {
    e.preventDefault();
    userData.message = messageInput.value.trim();
    // Create and display user message
    const messageContent = `<div class="message-text">${userData.Message}</div>`; // Use backticks for template literals
    const outgoingMessageDiv = createMessageElement(messageContent, "user-message");
    chatBody.appendChild(outgoingMessageDiv); 
};

// Handles pressing enter for sending messages
messageInput.addEventListener("keydown", (e) => {
    const userMessage = e.target.value.trim();
    if(e.key === "Enter" && userMessage) {
        handleOutgoingMessage(userMessage);
    }
});

sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e)) 