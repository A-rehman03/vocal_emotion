import React from 'react';
import ReactChatbot from './ReactChatbot';
import './ChatbotStyles.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>JTalk AI Voice Assistant</h1>
        <p>Powered by React + Python Flask API</p>
      </header>
      <main>
        <ReactChatbot />
      </main>
    </div>
  );
}

export default App;
