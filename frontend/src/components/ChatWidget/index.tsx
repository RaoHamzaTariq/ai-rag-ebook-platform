import React, { useState, useEffect } from 'react';
import ChatWindow from './ChatWindow';
import TextSelectionMenu from './TextSelectionMenu';
import styles from './styles.module.css';

import { useAuth } from '../../contexts/AuthContext';
import Link from '@docusaurus/Link';

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [selection, setSelection] = useState<{ text: string; top: number; left: number } | null>(null);
  const [windowProps, setWindowProps] = useState<{ initialMessage?: string; autoSubmit?: boolean; highlightedText?: string, agentType?: 'triage' | 'summarizer' | 'rag' }>({});

  const { isAuthenticated } = useAuth();
  // Handle text selection
  useEffect(() => {
    if (!isAuthenticated) return; // Don't handle selection if not logged in

    const handleMouseUp = () => {
      const windowSelection = window.getSelection();
      if (!windowSelection || windowSelection.isCollapsed) {
        setSelection(null);
        return;
      }

      const text = windowSelection.toString().trim();
      if (!text) {
        setSelection(null);
        return;
      }

      const range = windowSelection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      // Calculate position (viewport-relative, fixed positioning)
      const top = rect.top - 60; // 60px offset above selection
      const left = Math.max(10, Math.min(rect.left + (rect.width / 2) - 120, window.innerWidth - 250)); // Center with bounds

      // Only show if we are not inside the chat widget itself
      let node: Node | null = windowSelection.anchorNode;
      let isInsideChat = false;
      while (node) {
        if (node instanceof Element && node.classList.contains(styles.chatWidget)) {
          isInsideChat = true;
          break;
        }
        node = node.parentNode;
      }

      if (!isInsideChat) {
        setSelection({ text, top, left });
      }
    };

    document.addEventListener('mouseup', handleMouseUp);
    return () => document.removeEventListener('mouseup', handleMouseUp);
  }, [isAuthenticated]);

  const handleAddToChat = () => {
    if (!selection) return;
    setWindowProps({
      initialMessage: `> ${selection.text}\n\n`,
      autoSubmit: false,
      highlightedText: selection.text,
    });
    setIsOpen(true);
    setSelection(null);
    window.getSelection()?.removeAllRanges();
  };

  const handleSummarize = () => {
    if (!selection) return;

    const { text } = selection;

    // Normalize newlines and trim
    const cleaned = text.trim().replace(/\r\n/g, "\n");

    // Truncate to 2–3 lines or fallback to first 500 chars if no newlines
    let textToUse;
    const lines = cleaned.split("\n");

    if (cleaned.length > 500) {
      textToUse = lines.length >= 3
        ? lines.slice(0, 3).join("\n")
        : cleaned.slice(0, 500);
    } else {
      textToUse = cleaned;
    }

    setWindowProps({
      initialMessage: `Summarize this text:\n\n"${textToUse}"`,
      autoSubmit: true,
      highlightedText: text,     // full original text preserved
      agentType: 'summarizer'
    });

    setIsOpen(true);
    setSelection(null);
    window.getSelection()?.removeAllRanges();
  };


  const closeSelectionMenu = () => {
    setSelection(null);
    window.getSelection()?.removeAllRanges();
  }

  const toggleChat = () => {
    setIsOpen(!isOpen);
    // Clear special props when manually toggling
    if (!isOpen) {
      setWindowProps({});
    }
  };

  return (
    <>
      {selection && !isOpen && isAuthenticated && (
        <TextSelectionMenu
          position={{ top: selection.top, left: selection.left }}
          onAddToChat={handleAddToChat}
          onSummarize={handleSummarize}
          onClose={closeSelectionMenu}
        />
      )}
      <div className={styles.chatWidget}>
        {isOpen ? (
          isAuthenticated ? (
            <ChatWindow
              onClose={() => setIsOpen(false)}
              initialMessage={windowProps.initialMessage}
              autoSubmit={windowProps.autoSubmit}
              highlightedText={windowProps.highlightedText}
              agentType={windowProps.agentType}
            />
          ) : (
            <div className={styles.loginPromptContainer}>
              <div className={styles.loginPromptHeader}>
                <h3>Sign In Required</h3>
                <button
                  className={styles.closeButton}
                  onClick={() => setIsOpen(false)}
                  aria-label="Close"
                >
                  ×
                </button>
              </div>
              <div className={styles.loginPromptContent}>
                <p>Please sign in to access the AI RAG Assistant and ask questions about the book.</p>
                <Link to="/login" className="button button--primary button--block">
                  Sign In
                </Link>
                <div style={{ marginTop: '0.5rem', textAlign: 'center' }}>
                  <small>
                    Don't have an account? <Link to="/signup">Sign Up</Link>
                  </small>
                </div>
              </div>
            </div>
          )
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
    </>
  );
};

export default ChatWidget;