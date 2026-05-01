document.addEventListener("DOMContentLoaded", () => {

    const sendBtn = document.getElementById("sendBtn");
    const input = document.getElementById("userInput");

    sendBtn.addEventListener("click", sendMessage);

    input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") sendMessage();
    });

    async function sendMessage() {
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, "user");
        input.value = "";

        showTyping();

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            setTimeout(() => {
                removeTyping();
                addMessage(data.reply, "bot");
            }, 800);

        } catch (error) {
            removeTyping();
            addMessage("Server error 😅", "bot");
            console.error(error);
        }
    }

    function addMessage(text, sender) {
        const chatBox = document.getElementById("chatBox");

        const msg = document.createElement("div");
        msg.className = `message ${sender}`;

        const bubble = document.createElement("div");
        bubble.className = "bubble";
        bubble.innerText = text;

        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.innerText = sender === "bot" ? "🤖" : "👤";

        if (sender === "user") {
            msg.appendChild(bubble);
            msg.appendChild(avatar);
        } else {
            msg.appendChild(avatar);
            msg.appendChild(bubble);
        }

        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function showTyping() {
        const chatBox = document.getElementById("chatBox");

        const typing = document.createElement("div");
        typing.className = "message bot";
        typing.id = "typing";
        typing.innerHTML = "<div class='bubble'>Typing...</div>";

        chatBox.appendChild(typing);
    }

    function removeTyping() {
        const typing = document.getElementById("typing");
        if (typing) typing.remove();
    }

});