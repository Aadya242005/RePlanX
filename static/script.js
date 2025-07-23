function sendMessage() {
  const input = document.getElementById("user-input");
  const msg = input.value.trim();
  if (!msg) return;

  const chatBox = document.getElementById("chat-box");
  appendMessage("You", msg, "user");

  fetch("/get", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg }),
  })
    .then((res) => res.json())
    .then((data) => {
      appendMessage("Flexbot", data.reply, "bot");
    });

  input.value = "";
}

function appendMessage(sender, text, cls) {
  const chatBox = document.getElementById("chat-box");
  const msgDiv = document.createElement("div");
  msgDiv.className = cls;
  msgDiv.innerText = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function handleKey(e) {
  if (e.key === "Enter") sendMessage();
}

function quickAsk(msg) {
  document.getElementById("user-input").value = msg;
  sendMessage();
}
