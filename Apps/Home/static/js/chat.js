document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("open-chat-button").addEventListener("click", function() {
        document.getElementById("chat-popup").style.display = "block";
    });
    document.getElementById("close-chat-button").addEventListener("click", function() {
        document.getElementById("chat-popup").style.display = "none";
    });

    document.getElementById("send-button").addEventListener("click", function() {
        var userInput = document.getElementById("user-input").value;
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        if (userInput) {
            fetch("/chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ message: userInput }),
            })
            .then(response => response.json())
            .then(data => {
                var chatMessages = document.getElementById("chat-messages");
                chatMessages.innerHTML += "<div class='user-message'>" + userInput + "</div>";
                chatMessages.innerHTML += "<div class='bot-response'>" + data.response + "</div>";
                document.getElementById("user-input").value = "";
            });
        }
    });
});
