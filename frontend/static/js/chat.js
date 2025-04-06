document.getElementById("send-button").addEventListener("click", sendMessage);
document.getElementById("user-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") sendMessage();
});

async function sendMessage() {
  const input = document.getElementById("user-input");
  const text = input.value.trim();
  if (text === "") return;

  addMessage(text, 'user');
  input.value = "";

  try {
    const response = await fetch('/api/message/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    console.log('Server response:', data); 

    if (data && data.botResponse) {
      addMessage(data.botResponse, 'bot');
    } else if (data && data.error) {
      addMessage(`Server error: ${data.error}`, 'bot');
    } else {
      addMessage("Sorry, unexpected server response.", 'bot');
    }
  } catch (error) {
    console.error('Error:', error);
    addMessage("Error talking to server.", 'bot');
  }
}

function addMessage(text, sender) {
  const msg = document.createElement('div');
  msg.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
  msg.textContent = text;
  document.getElementById('messages').appendChild(msg);

  const chatWindow = document.getElementById('chat-window');
  chatWindow.scrollTop = chatWindow.scrollHeight;
}
