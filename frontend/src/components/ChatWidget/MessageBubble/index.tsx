import React from 'react';
import styles from './styles.module.css';

interface MessageBubbleProps {
  role: 'user' | 'agent';
  content: string;
  timestamp: Date;
  sources?: Array<{ slug: string, chapter_number: string, page_number: number, snippet: string }>;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ role, content, timestamp, sources }) => {
  const isUser = role === 'user';

  return (
    <div className={`${styles.messageBubble} ${isUser ? styles.userMessage : styles.agentMessage}`}>
      <div className={styles.messageContent}>
        <p>{content}</p>

        {sources && sources.length > 0 && (
          <div className={styles.sources}>
            <h4>Sources:</h4>
            <ul>
              {sources.map((source, index) => (
                <li key={index} className={styles.sourceItem}>
                  <a href={`${source.slug}`} className={styles.sourceLink} target="_blank" rel="noopener noreferrer">
                    <span className={styles.sourceChapter}>Chapter {source.chapter_number}</span>
                    {source.snippet && <span className={styles.sourceSnippet}>: {source.snippet.substring(0, 100)}{source.snippet.length > 100 ? '...' : ''}</span>}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
      <div className={styles.timestamp}>
        {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
};

export default MessageBubble;