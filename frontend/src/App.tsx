import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface Message {
  text: string;
  isUser: boolean;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const userId = useRef(`user-${Math.random().toString(36).substr(2, 9)}`);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    // Initial greeting
    handleSendMessage('');
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (userInput: string) => {
    try {
      if (userInput) {
        setMessages(prev => [...prev, { text: userInput, isUser: true }]);
      }
  
      setIsLoading(true);
      const response = await fetch('http://localhost:5002/ai-agent', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId.current,
          message: userInput,
        }),
      });
  
      // Log response for debugging
      console.log('Response Status:', response.status);
      console.log('Response Headers:', response.headers);
  
      const data = await response.json();
      console.log('API Response:', data);
  
      if (response.ok) {
        setMessages(prev => [...prev, { text: data.response, isUser: false }]);
      } else {
        throw new Error(data.error || 'Something went wrong');
      }
    } catch (error) {
      console.error('Error:', error); // Log the exact error
      setMessages(prev => [
        ...prev,
        {
          text: 'Sorry, there was an error processing your request. Please try again.',
          isUser: false,
        },
      ]);
    } finally {
      setIsLoading(false);
      setInput('');
    }
  };
  

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      handleSendMessage(input.trim());
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-2xl font-bold text-gray-900">Food Ordering Assistant</h1>
        </div>
      </header>

      <main className="flex-1 max-w-4xl w-full mx-auto p-4 flex flex-col">
        <div className="flex-1 bg-white rounded-lg shadow-md p-4 mb-4 overflow-y-auto max-h-[calc(100vh-16rem)]">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-2 ${
                    message.isUser
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  {message.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg px-4 py-2 text-gray-500">
                  Typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 rounded-lg border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            Send
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;