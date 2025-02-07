document.addEventListener("DOMContentLoaded", function () {
    const inputField = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
    const chatbox = document.getElementById("chatbox");
    const clearButton = document.getElementById("clear-btn");
    const darkModeButton = document.getElementById("dark-mode-btn");
    const voiceButton = document.getElementById("voice-btn");

    let darkMode = false;

    function sendMessage(message) {
        if (!message) {
            message = inputField.value.trim();
        }

        if (message === "") return;

        const userMessage = document.createElement("div");
        userMessage.className = "user-message p-2 rounded-lg self-end max-w-xs mt-2";
        userMessage.textContent = "You: " + message;
        chatbox.appendChild(userMessage);
        chatbox.scrollTop = chatbox.scrollHeight;

        inputField.value = ""; 

        fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            const botMessage = document.createElement("div");
            botMessage.className = "bot-message p-2 rounded-lg self-start max-w-xs mt-2";
            botMessage.textContent = "Bot: " + data.response;
            chatbox.appendChild(botMessage);
            chatbox.scrollTop = chatbox.scrollHeight;
        })
        .catch(error => console.error("Error:", error));
    }

    // Handle Enter Key Press
    inputField.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener("click", () => sendMessage());

    // Clear Chat Button
    clearButton.addEventListener("click", function () {
        chatbox.innerHTML = '<div class="text-center text-gray-500">Chat history cleared!</div>';
    });

    // Dark Mode Toggle
    darkModeButton.addEventListener("click", function () {
        document.body.classList.toggle("bg-gray-900");
        document.body.classList.toggle("text-white");
        darkMode = !darkMode;
        darkModeButton.textContent = darkMode ? "☀️ Light Mode" : "🌙 Dark Mode";
    });

    // Voice Input Functionality 🎤
    voiceButton.addEventListener("click", function () {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US"; // Set language
        recognition.start();

        recognition.onstart = function () {
            voiceButton.textContent = "🎙️ Listening...";
            voiceButton.classList.add("bg-red-500");
        };

        recognition.onspeechend = function () {
            recognition.stop();
            voiceButton.textContent = "🎤";
            voiceButton.classList.remove("bg-red-500");
        };

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            inputField.value = transcript;
            sendMessage(transcript);
        };

        recognition.onerror = function () {
            voiceButton.textContent = "🎤";
            voiceButton.classList.remove("bg-red-500");
        };
    });
});
