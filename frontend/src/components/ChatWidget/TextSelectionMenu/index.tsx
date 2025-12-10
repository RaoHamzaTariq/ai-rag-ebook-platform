import React from 'react';
import styles from './styles.module.css';

interface TextSelectionMenuProps {
    position: { top: number; left: number };
    onAddToChat: () => void;
    onSummarize: () => void;
    onClose: () => void;
}

const TextSelectionMenu: React.FC<TextSelectionMenuProps> = ({
    position,
    onAddToChat,
    onSummarize,
    onClose,
}) => {
    // Prevent menu clicks from closing the selection clearing
    const handleMouseDown = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
    };

    return (
        <div
            className={styles.menuContainer}
            style={{ top: position.top, left: position.left }}
            onMouseDown={handleMouseDown}
        >
            <button className={styles.menuButton} onClick={onAddToChat}>
                💬 Add to chat
            </button>
            <button className={`${styles.menuButton} ${styles.primary}`} onClick={onSummarize}>
                ✨ Summarize
            </button>
            <button className={styles.menuButton} onClick={onClose} aria-label="Close menu">
                ✕
            </button>
        </div>
    );
};

export default TextSelectionMenu;
