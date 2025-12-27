import React from 'react';
import clsx from 'clsx';
import styles from './InteractiveCodeBlock.module.css';

interface Props {
  children: React.ReactNode;
  title?: string;
  language?: string;
  showLineNumbers?: boolean;
}

const InteractiveCodeBlock = ({
  children,
  title,
  language = 'python',
  showLineNumbers = false,
}: Props): React.ReactElement => {
  return (
    <div className={clsx('code-block-wrapper', styles.wrapper)}>
      {title && (
        <div className={clsx('code-block-header', styles.header)}>
          <span className={styles.title}>{title}</span>
          <span className={styles.language}>{language}</span>
        </div>
      )}
      <div className={clsx('code-block-content', styles.content)}>
        <pre className={showLineNumbers ? 'line-numbers' : ''}>
          <code className={`language-${language}`}>
            {children}
          </code>
        </pre>
      </div>
    </div>
  );
};

export default InteractiveCodeBlock;