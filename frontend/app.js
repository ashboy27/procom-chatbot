const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("chat-form");
const questionEl = document.getElementById("question");
const sendBtn = document.getElementById("send-btn");
const clearBtn = document.getElementById("clear-btn");
const updateKbBtn = document.getElementById("update-kb-btn");

const API_URL = "http://localhost:3000/ask";
const UPDATE_KB_URL = "http://localhost:3000/update-knowledge";
const history = [];

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function addMessage(role, content) {
  const message = document.createElement("div");
  message.className = `message ${role}`;
  message.textContent = content;
  messagesEl.appendChild(message);
  scrollToBottom();
}

function setBusy(isBusy) {
  sendBtn.disabled = isBusy;
  clearBtn.disabled = isBusy;
  questionEl.disabled = isBusy;
}

function resetChat() {
  history.length = 0;
  messagesEl.innerHTML = "";
  addMessage("system", "Conversation cleared. Ask the next question.");
}

addMessage("system", "Start by asking a PROCOM-related question.");

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionEl.value.trim();
  if (!question) {
    return;
  }

  questionEl.value = "";
  addMessage("user", question);
  history.push({ role: "user", content: question });

  setBusy(true);
  addMessage("assistant", "Thinking...");
  const thinkingNode = messagesEl.lastElementChild;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        history,
      }),
    });

    const payload = await response.json();
    const answer = payload.answer || "No answer returned.";

    thinkingNode.textContent = answer;
    history.push({ role: "assistant", content: answer });
  } catch (error) {
    thinkingNode.textContent = "Failed to reach the backend. Check that the API is running on port 3000.";
    history.push({
      role: "assistant",
      content: "Failed to reach the backend. Check that the API is running on port 3000.",
    });
  } finally {
    setBusy(false);
    questionEl.focus();
    scrollToBottom();
  }
});

clearBtn.addEventListener("click", resetChat);

updateKbBtn.addEventListener("click", async () => {
  updateKbBtn.disabled = true;
  addMessage("system", "Updating knowledge base...");

  try {
    const response = await fetch(UPDATE_KB_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const payload = await response.json();
    if (payload.status === "success") {
      addMessage("system", "✓ Knowledge base updated successfully!");
    } else {
      addMessage("system", `✗ Knowledge base update failed: ${payload.message}`);
    }
  } catch (error) {
    addMessage("system", "✗ Failed to update knowledge base. Is the backend running?");
  } finally {
    updateKbBtn.disabled = false;
  }
});
