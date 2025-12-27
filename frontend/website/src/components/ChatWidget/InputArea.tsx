import React, { useState, KeyboardEvent } from 'react';
import styles from './ChatWidget.module.css';

interface InputAreaProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

const InputArea: React.FC<InputAreaProps> = ({ onSendMessage, disabled }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSend = () => {
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={styles.chatInputArea}>
      <textarea
        className={styles.chatInput}
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask a question about the book..."
        disabled={disabled}
        rows={1}
      />
      <button
        className={styles.sendButton}
        onClick={handleSend}
        disabled={disabled || !inputValue.trim()}
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M22 2L11 13M22 2L15 22L11 13M11 13L2 9L22 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </div>
  );
};

export default InputArea;