import React, { useState, useEffect, useRef } from 'react';
import Message from './Message';
import InputArea from './InputArea';
import styles from './ChatWidget.module.css';

interface MessageData {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    source_path: string;
    source_title: string;
    relevance_score: number;
  }>;
  followup_questions?: string[];
}

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [sessionId, setSessionId] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Initialize session ID on component mount
  useEffect(() => {
    // Generate a new session ID if one doesn't exist
    if (!sessionId) {
      setSessionId(generateSessionId());
    }
  }, []);

  // Scroll to bottom of messages when new messages are added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const generateSessionId = (): string => {
    return 'session_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Add user message to the chat
    const userMessage: MessageData = {
      id: Date.now().toString(),
      role: 'user',
      content: content,
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Call the backend API
      const response = await fetch('http://localhost:8000/api/v1/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: content,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Add assistant message to the chat
      const assistantMessage: MessageData = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        sources: data.sources,
        followup_questions: data.followup_questions,
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSessionId(data.session_id); // Update session ID if it changed
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to get response. Please try again.');

      // Add error message to the chat
      const errorMessage: MessageData = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFollowupClick = (question: string) => {
    handleSendMessage(question);
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <>
      {!isOpen && (
        <button className={styles.chatToggleButton} onClick={toggleChat}>
          💬
        </button>
      )}

      {isOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatHeader}>
            <h3 className={styles.chatTitle}>Book Assistant</h3>
            <button className={styles.closeButton} onClick={closeChat}>
              ×
            </button>
          </div>
          <div className={styles.chatBody}>
            {messages.length === 0 ? (
              <div className={styles.message + ' ' + styles.assistantMessage}>
                Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics book.
                Ask me any questions about the content and I'll help you find answers.
              </div>
            ) : (
              messages.map((msg) => (
                <Message
                  key={msg.id}
                  role={msg.role}
                  content={msg.content}
                  sources={msg.sources}
                  followup_questions={msg.followup_questions}
                  onFollowupClick={handleFollowupClick}
                />
              ))
            )}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistantMessage} ${styles.loadingIndicator}`}>
                Thinking...
              </div>
            )}
            {error && (
              <div className={styles.error}>
                {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <InputArea onSendMessage={handleSendMessage} disabled={isLoading} />
        </div>
      )}
    </>
  );
};

export default ChatWidget;