// frontend/src/components/history/ConversationViewer.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { MessageBubble } from '../ChatWidget/MessageBubble';
import styles from './styles.module.css';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  sources?: Array<{slug: string; chapter_number: string; page_number: number; snippet: string}>;
}

export const ConversationViewer: React.FC = () => {
  const { conversationId } = useParams<{ conversationId: string }>();
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchConversation = async () => {
      try {
        // This would be replaced with a real API call to get conversation details
        // const response = await fetch(`/api/conversations/${conversationId}`);
        // const data = await response.json();

        // Mock data for now
        const mockMessages: Message[] = [
          {
            id: '1',
            role: 'user',
            content: 'What is RAG in AI systems?',
            timestamp: '2025-12-17T10:30:00Z',
          },
          {
            id: '2',
            role: 'assistant',
            content: 'RAG stands for Retrieval-Augmented Generation. It\'s a technique that combines a retrieval system with a generative model to provide more accurate and contextually relevant responses.',
            timestamp: '2025-12-17T10:31:00Z',
            sources: [
              {
                slug: 'handbook',
                chapter_number: '3.2',
                page_number: 45,
                snippet: 'RAG systems retrieve relevant documents and use them to inform the generation of responses...'
              }
            ]
          },
          {
            id: '3',
            role: 'user',
            content: 'How does it improve accuracy?',
            timestamp: '2025-12-17T10:32:00Z',
          },
          {
            id: '4',
            role: 'assistant',
            content: 'By retrieving relevant information from a knowledge base, RAG systems can provide more factually accurate responses that are grounded in specific documents rather than relying solely on the model\'s pre-trained knowledge.',
            timestamp: '2025-12-17T10:33:00Z',
            sources: [
              {
                slug: 'handbook',
                chapter_number: '3.4',
                page_number: 52,
                snippet: 'The retrieval component finds relevant documents that contain information related to the user query...'
              }
            ]
          },
        ];

        setMessages(mockMessages);
      } catch (err) {
        setError('Failed to load conversation');
        console.error('Error fetching conversation:', err);
      } finally {
        setLoading(false);
      }
    };

    if (conversationId) {
      fetchConversation();
    }
  }, [conversationId]);

  if (loading) return <div className={styles.loading}>Loading conversation...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.conversationViewer}>
      <div className={styles.messagesContainer}>
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            role={message.role}
            content={message.content}
            timestamp={new Date(message.timestamp).toLocaleTimeString()}
            sources={message.sources}
          />
        ))}
      </div>
    </div>
  );
};