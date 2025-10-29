

import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    // Check system status on load
    checkSystemStatus();
    
    // Add welcome message
    setMessages([{
      id: 1,
      type: 'bot',
      content: 'Welcome to LawBot! I can help you with questions about Indian law. Ask me anything about IPC, CrPC, Constitution, or other legal matters.',
      timestamp: new Date().toISOString()
    }]);
  }, []);

  const checkSystemStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Failed to check system status:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          conversation_history: messages.map(msg => ({
            role: msg.type === 'user' ? 'user' : 'assistant',
            content: msg.content
          }))
        }),
      });

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: data.response,
        citations: data.citations || [],
        toolsUsed: data.tools_used || [],
        confidence: data.confidence,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Failed to send message:', error);
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const exampleQuestions = [
    "What is IPC Section 302?",
    "How do I file a criminal complaint?",
    "What is the procedure for bail?",
    "Explain the concept of arrest under CrPC"
  ];

  return (
    <div className="App">
      <header className="App-header">
        <h1>LawBot - Legal Q&A Assistant</h1>
        <div className="status-indicator">
          {systemStatus && (
            <span className={`status ${systemStatus.status}`}>
              {systemStatus.status === 'healthy' ? '🟢 Online' : '🟡 Limited Mode'}
            </span>
          )}
        </div>
      </header>

      <div className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-content">
                {message.content}
              </div>
              
              {message.citations && message.citations.length > 0 && (
                <div className="citations">
                  <strong>Sources:</strong> {message.citations.join(', ')}
                </div>
              )}
              
              {message.toolsUsed && message.toolsUsed.length > 0 && (
                <div className="tools-used">
                  <strong>Tools Used:</strong> {message.toolsUsed.map(tool => tool.tool).join(', ')}
                </div>
              )}
              
              {message.confidence && (
                <div className={`confidence ${message.confidence}`}>
                  Confidence: {message.confidence}
                </div>
              )}
              
              <div className="timestamp">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message bot">
              <div className="loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                LawBot is thinking...
              </div>
            </div>
          )}
        </div>

        <div className="input-container">
          <div className="example-questions">
            <p>Try these examples:</p>
            {exampleQuestions.map((question, index) => (
              <button
                key={index}
                className="example-btn"
                onClick={() => setInputValue(question)}
              >
                {question}
              </button>
            ))}
          </div>
          
          <div className="input-row">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a legal question..."
              disabled={isLoading}
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="send-btn"
            >
              Send
            </button>
          </div>
        </div>
      </div>

      <footer className="disclaimer">
        <p>
          ⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. 
          LawBot provides general legal information, not professional legal advice. 
          Always consult a qualified lawyer for legal matters.
        </p>
      </footer>
    </div>
  );
}

export default App;
