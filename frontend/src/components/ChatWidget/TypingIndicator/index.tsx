import React from 'react';
import styles from './styles.module.css';

const TypingIndicator: React.FC = () => {
  return (
    <div className={styles.typingIndicator}>
      <div className={styles.messageBubble}>
        <div className={styles.dots}>
          <div className={styles.dot}></div>
          <div className={styles.dot}></div>
          <div className={styles.dot}></div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;