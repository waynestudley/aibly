import React, { useState } from 'react';
import axios from 'axios';

export default function Chat() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [model, setModel] = useState('openai');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      const res = await axios.post('/ask', {
        question: query,
        model: model
      });
      setResponse(res.data.answer);
    } catch (err) {
      console.error(err);
      setResponse('Error getting response. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Ask About Aibly</h2>
      
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Model:
        </label>
        <select 
          value={model} 
          onChange={(e) => setModel(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-aibly-orange focus:border-aibly-orange"
        >
          <option value="openai">OpenAI GPT-3.5</option>
          <option value="huggingface">Hugging Face Flan-T5</option>
        </select>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="What would you like to know about Aibly?"
          className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-aibly-orange focus:border-aibly-orange"
        />
        
        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full bg-aibly-orange text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Thinking...' : 'Ask Question'}
        </button>
      </form>

      {response && (
        <div className="mt-6 p-4 bg-gray-50 rounded-md border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-2">Answer:</h3>
          <p className="text-gray-700 whitespace-pre-wrap">{response}</p>
        </div>
      )}
    </div>
  );
}