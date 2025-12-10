import React, { useState } from 'react';
import ChatWindow from './ChatWindow';
import styles from './styles.module.css';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.chatWidget}>
      {isOpen ? (
        <ChatWindow onClose={() => setIsOpen(false)} />
      ) : (
        <button
          className={styles.fabButton}
          onClick={toggleChat}
          aria-label="Open chat"
        >
          💬
        </button>
      )}
    </div>
  );
};

export default ChatWidget;