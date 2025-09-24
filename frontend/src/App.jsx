import { useState } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const API_BASE_URL = window.location.origin + '/api'

  const sendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage = { type: 'user', text: inputValue }
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: inputValue })
      })

      setIsLoading(false)

      if (!res.ok) {
        const errorText = await res.text()
        const errorMessage = { type: 'bot', text: `Error ${res.status}: ${errorText}`, isError: true }
        setMessages(prev => [...prev, errorMessage])
        return
      }

      const data = await res.json()
      const botMessage = { type: 'bot', text: data.response || 'No response', audio: data.audio }
      setMessages(prev => [...prev, botMessage])

      // TTS playback
      if (data.audio) {
        const audio = new Audio("data:audio/mpeg;base64," + data.audio)
        audio.play()
      }
    } catch (error) {
      setIsLoading(false)
      const errorMessage = { type: 'bot', text: `Network error: ${error.message}`, isError: true }
      setMessages(prev => [...prev, errorMessage])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage()
    }
  }

  return (
    <div className="app">
      <h1>PSI 20 Chatbot</h1>
      <p>This chatbot provides information about PSI 20 companies using Retrieval-Augmented Generation (RAG) with Azure AI Search and OpenAI GPT models. Ask questions about Portuguese stock market companies!</p>

      <div className="chat-container">
        <div className="chat">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <strong>{message.type === 'user' ? 'You:' : 'Bot:'}</strong> {message.text}
            </div>
          ))}
          {isLoading && <div className="message bot loading">Loading...</div>}
        </div>

        <div className="input-container">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your question..."
            disabled={isLoading}
          />
          <button onClick={sendMessage} disabled={isLoading || !inputValue.trim()}>
            Send
          </button>
        </div>
      </div>

      <footer>
        <a href="https://github.com/afelix-95/GenAI-RAG-App" target="_blank" rel="noopener noreferrer">
          View source code on GitHub
        </a>
      </footer>
    </div>
  )
}

export default App
