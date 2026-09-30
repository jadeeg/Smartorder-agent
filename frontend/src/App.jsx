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

    const conversation = [...messages, { sender: "user", text }];

    setMessages((current) => [
      ...current,
      {
        sender: "user",
        text,
      },
    ]);

    setInput("");

    try {
      const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: conversation.map((message) => ({
            role: message.sender === "bot" ? "assistant" : "user",
            content: message.text,
          })),
        }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "SmartOrder request failed");
      }

      setMessages((current) => [
        ...current,
        {
          sender: "bot",
          text: data.response,
        },
      ]);
    } catch {
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
