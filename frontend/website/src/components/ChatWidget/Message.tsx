import React from 'react';
import styles from './ChatWidget.module.css';

interface MessageProps {
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    source_path: string;
    source_title: string;
    relevance_score: number;
  }>;
  followup_questions?: string[];
  onFollowupClick?: (question: string) => void;
}

const Message: React.FC<MessageProps> = ({
  role,
  content,
  sources,
  followup_questions,
  onFollowupClick
}) => {
  const isUser = role === 'user';
  const messageClass = isUser
    ? `${styles.message} ${styles.userMessage}`
    : `${styles.message} ${styles.assistantMessage}`;

  return (
    <div className={messageClass}>
      {content}
      {sources && sources.length > 0 && (
        <div className={styles.sources}>
          <strong>Sources:</strong>
          <ul>
            {sources.map((source, index) => (
              <li key={index}>
                {source.source_title} ({(source.relevance_score * 100).toFixed(1)}% relevance)
              </li>
            ))}
          </ul>
        </div>
      )}
      {followup_questions && followup_questions.length > 0 && onFollowupClick && (
        <div className={styles.followupQuestions}>
          <strong>Follow-up questions:</strong>
          <ul>
            {followup_questions.map((question, index) => (
              <li key={index} onClick={() => onFollowupClick(question)}>
                {question}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Message;