// frontend/src/components/history/ConversationList.tsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from './styles.module.css';

interface Conversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
}

export const ConversationList: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [filteredConversations, setFilteredConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const conversationsPerPage = 10;

  useEffect(() => {
    const fetchConversations = async () => {
      try {
        // This would be replaced with a real API call to get user's conversations
        // const response = await fetch('/api/conversations');
        // const data = await response.json();

        // Mock data for now
        const mockConversations: Conversation[] = [
          {
            id: '1',
            title: 'Understanding RAG Systems',
            created_at: '2025-12-17T10:30:00Z',
            updated_at: '2025-12-17T11:45:00Z',
          },
          {
            id: '2',
            title: 'Chatbot Architecture',
            created_at: '2025-12-16T09:15:00Z',
            updated_at: '2025-12-16T14:20:00Z',
          },
          {
            id: '3',
            title: 'Database Design Patterns',
            created_at: '2025-12-15T16:45:00Z',
            updated_at: '2025-12-15T17:30:00Z',
          },
          {
            id: '4',
            title: 'AI Ethics and Safety',
            created_at: '2025-12-14T12:30:00Z',
            updated_at: '2025-12-14T13:45:00Z',
          },
          {
            id: '5',
            title: 'Machine Learning Fundamentals',
            created_at: '2025-12-13T08:15:00Z',
            updated_at: '2025-12-13T09:30:00Z',
          },
          {
            id: '6',
            title: 'Natural Language Processing',
            created_at: '2025-12-12T15:20:00Z',
            updated_at: '2025-12-12T16:40:00Z',
          },
          {
            id: '7',
            title: 'Computer Vision Techniques',
            created_at: '2025-12-11T11:10:00Z',
            updated_at: '2025-12-11T12:25:00Z',
          },
          {
            id: '8',
            title: 'Reinforcement Learning',
            created_at: '2025-12-10T14:05:00Z',
            updated_at: '2025-12-10T15:15:00Z',
          },
          {
            id: '9',
            title: 'Deep Learning Architectures',
            created_at: '2025-12-09T10:00:00Z',
            updated_at: '2025-12-09T11:20:00Z',
          },
          {
            id: '10',
            title: 'Data Preprocessing Methods',
            created_at: '2025-12-08T13:30:00Z',
            updated_at: '2025-12-08T14:45:00Z',
          },
          {
            id: '11',
            title: 'Model Evaluation Metrics',
            created_at: '2025-12-07T09:15:00Z',
            updated_at: '2025-12-07T10:30:00Z',
          },
          {
            id: '12',
            title: 'Hyperparameter Tuning',
            created_at: '2025-12-06T16:45:00Z',
            updated_at: '2025-12-06T17:55:00Z',
          },
        ];

        setConversations(mockConversations);
      } catch (err) {
        setError('Failed to load conversations');
        console.error('Error fetching conversations:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchConversations();
  }, []);

  // Filter conversations based on search term
  useEffect(() => {
    const filtered = conversations.filter(conversation =>
      conversation.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredConversations(filtered);
    setCurrentPage(1); // Reset to first page when search changes
  }, [conversations, searchTerm]);

  // Pagination
  const indexOfLastConversation = currentPage * conversationsPerPage;
  const indexOfFirstConversation = indexOfLastConversation - conversationsPerPage;
  const currentConversations = filteredConversations.slice(indexOfFirstConversation, indexOfLastConversation);
  const totalPages = Math.ceil(filteredConversations.length / conversationsPerPage);

  const handlePageChange = (pageNumber: number) => {
    setCurrentPage(pageNumber);
  };

  if (loading) return <div className={styles.loading}>Loading conversations...</div>;
  if (error) return <div className={styles.error}>{error}</div>;

  return (
    <div className={styles.conversationList}>
      <h3>Recent Conversations</h3>

      {/* Search input */}
      <div className={styles.searchContainer}>
        <input
          type="text"
          placeholder="Search conversations..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className={styles.searchInput}
        />
      </div>

      <ul className={styles.list}>
        {currentConversations.map((conversation) => (
          <li key={conversation.id} className={styles.listItem}>
            <Link to={`/chat/${conversation.id}`} className={styles.conversationLink}>
              <div className={styles.conversationTitle}>{conversation.title}</div>
              <div className={styles.conversationDate}>
                {new Date(conversation.updated_at).toLocaleDateString()}
              </div>
            </Link>
          </li>
        ))}
      </ul>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className={styles.pagination}>
          {Array.from({ length: totalPages }, (_, index) => index + 1).map((page) => (
            <button
              key={page}
              onClick={() => handlePageChange(page)}
              className={`${styles.pageButton} ${currentPage === page ? styles.activePage : ''}`}
            >
              {page}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};