import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import MessageBubble from '../MessageBubble';
import TypingIndicator from '../TypingIndicator';
import { agentClient, type AgentResponse } from './../../../services/agentClient';
import styles from './styles.module.css';

interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
  sources?: Array<{ slug: string, chapter_number: string, page_number: number, snippet: string }>;
}

export interface ChatWindowProps {
  onClose: () => void;
  initialMessage?: string;
  autoSubmit?: boolean;
  highlightedText?: string;
  agentType?: 'triage' | 'summarizer' | 'rag';
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onClose, initialMessage, autoSubmit, highlightedText , agentType}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState(initialMessage || '');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const hasAutoSubmitted = useRef(false);

  // Generate session ID on component mount
  useEffect(() => {
    const id = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(id);
  }, []);

  // Handle auto-submit if requested (only once)
  useEffect(() => {
    if (autoSubmit && initialMessage && !hasAutoSubmitted.current && sessionId) {
      hasAutoSubmitted.current = true;
      handleSendMessage(initialMessage, true);
    } else if (initialMessage && !hasAutoSubmitted.current) {
      // Just set the input value if not auto-submitting
      setInputValue(initialMessage);
    }
  }, [initialMessage, autoSubmit, sessionId]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (textOverride?: string, isAutoSubmit: boolean = false) => {
    const textToSend = textOverride || inputValue;
    if (!textToSend.trim() || (isLoading && !isAutoSubmit)) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: `msg_${Date.now()}`,
      role: 'user',
      content: textToSend,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    if (!isAutoSubmit) setInputValue('');
    setIsLoading(true);

    try {
      // Get current page context
      const currentPage = location.pathname;

      // Determine agent type based on content (simple heuristic or explicit override could be added later)
      // For now, if auto-submit is true and it looks like a summarization request, we might want to hint the backend?
      // But the backend has a Triage agent. So we just send it to Triage.
      // If the user clicked "Summarize", the textToSend will likely be "Summarize this: ..."

      const response = await agentClient.runAgent({
        agent_type:  agentType || 'triage',
        query: textToSend,
        current_page: currentPage,
        highlighted_text: highlightedText,
        session_id: sessionId
      });

      // Add agent response to the chat
      const agentMessage: Message = {
        id: `msg_${Date.now()}`,
        role: 'agent',
        content: response.message,
        timestamp: new Date(),
        sources: response.sources || []
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to the chat
      const errorMessage: Message = {
        id: `msg_${Date.now()}`,
        role: 'agent',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className={styles.chatWindow}>
      <div className={styles.header}>
        <h3>AI Assistant</h3>
        <button
          className={styles.closeButton}
          onClick={onClose}
          aria-label="Close chat"
        >
          ×
        </button>
      </div>

      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <div className={styles.welcomeMessage}>
            <p>Hello! I'm your AI assistant. How can I help you with this book?</p>
          </div>
        ) : (
          messages.map((message) => (
            <MessageBubble
              key={message.id}
              role={message.role}
              content={message.content}
              timestamp={message.timestamp}
              sources={message.sources}
            />
          ))
        )}

        {isLoading && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.inputContainer}>
        <textarea
          className={styles.textInput}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about this book..."
          rows={1}
          aria-label="Type your message"
        />
        <button
          className={styles.sendButton}
          onClick={() => handleSendMessage()}
          disabled={!inputValue.trim() || isLoading}
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;