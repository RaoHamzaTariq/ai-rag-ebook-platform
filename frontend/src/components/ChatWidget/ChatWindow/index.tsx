import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from '@docusaurus/router';
import MessageBubble from '../MessageBubble';
import TypingIndicator from '../TypingIndicator';
import { authClient } from './../../../lib/authClient';
import siteConfig from '@generated/docusaurus.config';
import { agentClient, type AgentResponse } from './../../../services/agentClient';
import styles from './styles.module.css';
import { useAuth } from './../../../contexts/AuthContext';
import Link from '@docusaurus/Link';

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
  conversationId?: string; // Optional conversation ID for loading existing conversation
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  onClose,
  initialMessage,
  autoSubmit,
  highlightedText,
  agentType,
  conversationId
}) => {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState(initialMessage || '');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [conversationTitle, setConversationTitle] = useState<string>('New Conversation');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const location = useLocation();
  const hasAutoSubmitted = useRef(false);

  // Use conversationId if provided, otherwise generate a new session ID
  useEffect(() => {
    if (conversationId) {
      setSessionId(conversationId);
      // Set a default title based on the conversation ID or load from API
      setConversationTitle(`Conversation ${conversationId.substring(0, 8)}`);
    } else {
      const id = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      setSessionId(id);
    }
  }, [conversationId]);

  // Load conversation history if conversationId is provided
  useEffect(() => {
    if (conversationId) {
      const loadConversation = async () => {
        try {
          const baseUrl = (siteConfig.customFields?.backendUrl as string) || 'http://localhost:8000';
          const headers: Record<string, string> = {
            'Content-Type': 'application/json',
          };

          // Try to get token for auth
          try {
            const tokenResult = await authClient.token();
            if (tokenResult?.data?.token) {
              headers['Authorization'] = `Bearer ${tokenResult.data.token}`;
            }
          } catch (e) {
            console.log("No token available for history loading");
          }

          // Also include X-User-ID if we have a session
          const { data: session } = await authClient.getSession();
          if (session?.user?.id) {
            headers['X-User-ID'] = session.user.id;
          }

          const response = await fetch(`${baseUrl}/conversations/${conversationId}/messages`, {
            headers
          });

          if (!response.ok) {
            throw new Error(`Failed to load history: ${response.status}`);
          }

          const data = await response.json();

          // Map backend message format to frontend format
          const formattedMessages: Message[] = data.map((msg: any) => ({
            id: msg.id || `msg_${Date.now()}_${Math.random()}`,
            role: msg.role === 'assistant' ? 'agent' : msg.role,
            content: msg.content,
            timestamp: new Date(msg.created_at || msg.timestamp),
            sources: msg.sources || []
          }));

          setMessages(formattedMessages);
        } catch (error) {
          console.error('Error loading conversation:', error);
        }
      };

      loadConversation();
    }
  }, [conversationId]);

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

    // If this is the first message in a new conversation, use it to set the title
    if (messages.length === 0) {
      setConversationTitle(textToSend.substring(0, 30) + (textToSend.length > 30 ? '...' : ''));
    }

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

      const response = await agentClient.runAgent({
        agent_type: agentType || 'triage',
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

  // Function to start a new conversation
  const startNewConversation = () => {
    setMessages([]);
    setConversationTitle('New Conversation');
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    setSessionId(newSessionId);
    setInputValue('');
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
        <div className={styles.headerLeft}>
          <h3>{conversationTitle}</h3>
        </div>
        <div className={styles.headerRight}>
          <button
            className={styles.newConversationButton}
            onClick={startNewConversation}
            title="Start new conversation"
            aria-label="New conversation"
          >
            + New
          </button>
          <button
            className={styles.closeButton}
            onClick={onClose}
            aria-label="Close chat"
          >
            ×
          </button>
        </div>
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
        {!isAuthenticated ? (
          <div className={styles.authPrompt}>
            <p>Please <Link to="/login">sign in</Link> to use the AI assistant.</p>
          </div>
        ) : (
          <>
            <textarea
              className={styles.textInput}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about this book..."
              rows={1}
              aria-label="Type your message"
              disabled={authLoading}
            />
            <button
              className={styles.sendButton}
              onClick={() => handleSendMessage()}
              disabled={!inputValue.trim() || isLoading || authLoading}
              aria-label="Send message"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default ChatWindow;