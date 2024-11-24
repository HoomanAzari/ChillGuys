const chatBody = document.querySelector(".chat-body");
const messageInput = document.querySelector(".message-input");
const sendMessageButton = document.querySelector("#send-message");
const chatbotToggler = document.querySelector("#chatbot-toggler");
const closeChatbot = document.querySelector("#close-chatbot");

const userData = {
    message: null,
};

const chatHistory = []; // Keeps track of the chat history

const initialInputHeight = messageInput.scrollHeight;

// Create a message element with dynamic classes and return it
const createMessageElement = (content, ...classes) => {
    const div = document.createElement("div");
    div.classList.add("message", ...classes);
    div.innerHTML = content;
    return div;
};

// Generate the response using Flask
const generateBotResponse = async (incomingMessageDiv) => {
    const messageElement = incomingMessageDiv.querySelector(".message-text");

    try {
        // Send a POST request to the Flask backend
        const response = await fetch("/generate-response", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: userData.message,
                chat_history: chatHistory, // Include previous messages
            }),
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.error || "An unknown error occurred");

        // Extract bot response and display it
        const botResponse = data.bot_response;
        messageElement.innerText = botResponse;

        // Add the bot response to chat history
        chatHistory.push({ role: "assistant", text: botResponse });
    } catch (error) {
        console.error(error);
        messageElement.innerText = error.message;
        messageElement.style.color = "#ff0000";
    } finally {
        incomingMessageDiv.classList.remove("thinking");
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
    }
};

// Handles outgoing user messages
const handleOutgoingMessage = (e) => {
    e.preventDefault();

    userData.message = messageInput.value.trim();
    if (!userData.message) return; // Prevent sending empty messages

    // Clear the input field after the message is sent
    messageInput.value = "";
    messageInput.dispatchEvent(new Event("input"));

    // Create and display the user's message
    const messageContent = `<div class="message-text"></div>`;
    const outgoingMessageDiv = createMessageElement(messageContent, "user-message");
    outgoingMessageDiv.querySelector(".message-text").innerText = userData.message;
    chatBody.appendChild(outgoingMessageDiv);

    // Add the user's message to chat history
    chatHistory.push({ role: "user", text: userData.message });

    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

    // Show the thinking indicator and generate the bot's response
    setTimeout(() => {
        const botMessageContent = `
            <img class="bot-avatar" src="/frontend/chill-guy.png" alt="Chill Guy Avatar" width="50" height="50">
            <div class="message-text">
                <div class="thinking-indicator">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>`;
        const incomingMessageDiv = createMessageElement(botMessageContent, "bot-message", "thinking");
        chatBody.appendChild(incomingMessageDiv);
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
        generateBotResponse(incomingMessageDiv);
    }, 600);
};

// Adjust the height of the chat input dynamically
messageInput.addEventListener("input", () => {
    messageInput.style.height = `${initialInputHeight}px`;
    messageInput.style.height = `${messageInput.scrollHeight}px`;
    document.querySelector(".chat-form").style.borderRadius =
        messageInput.scrollHeight > initialInputHeight ? "15px" : "32px";
});

// Handle pressing Enter for sending messages
messageInput.addEventListener("keydown", (e) => {
    const userMessage = e.target.value.trim();
    if (e.key === "Enter" && userMessage && !e.shiftKey) {
        handleOutgoingMessage(e);
    }
});

// Event listeners for buttons
sendMessageButton.addEventListener("click", (e) => handleOutgoingMessage(e));
chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
closeChatbot.addEventListener("click", () => document.body.classList.remove("show-chatbot"));