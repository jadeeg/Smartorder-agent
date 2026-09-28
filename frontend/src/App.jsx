import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! I'm the SmartOrder assistant. How can I help you today?",
    },
  ]);

  const [input, setInput] = useState("");

const handleSend = async () => {
  const text = input.trim();

  if (!text) return;

  setMessages((current) => [
    ...current,
    {
      sender: "user",
      text,
    },
  ]);

  setInput("");

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: text,
      }),
    });

    const data = await response.json();

    setMessages((current) => [
      ...current,
      {
        sender: "bot",
        text: data.response,
      },
    ]);
  } catch (error) {
    setMessages((current) => [
      ...current,
      {
        sender: "bot",
        text: "Sorry, I couldn't connect to SmartOrder.",
      },
    ]);
  }
}; 

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="app">
      <div className="chat-container">
        <header className="chat-header">
          <div>
            <h1>SmartOrder</h1>
            <span>Customer Support</span>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            Online
          </div>
        </header>

        <main className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </main>

        <div className="input-area">
          <input
            type="text"
            placeholder="Ask about your order..."
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={handleKeyDown}
          />

          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
