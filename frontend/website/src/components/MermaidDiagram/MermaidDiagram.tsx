import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';
import styles from './MermaidDiagram.module.css';

interface Props {
  chart: string;
  alt?: string;
  title?: string;
}

const MermaidDiagram = ({ chart, alt = 'Mermaid diagram', title }: Props): React.ReactElement => {
  const containerRef = useRef<HTMLDivElement>(null);
  const id = useRef(`mermaid-${Math.random().toString(36).substr(2, 9)}`);

  useEffect(() => {
    const renderDiagram = async () => {
      if (containerRef.current) {
        try {
          mermaid.initialize({
            startOnLoad: false,
            theme: 'default',
            securityLevel: 'loose',
          });

          const { svg, bindFunctions } = await mermaid.render(id.current, chart);
          containerRef.current.innerHTML = svg;
          if (bindFunctions) bindFunctions(containerRef.current);
        } catch (error) {
          console.error('Error rendering Mermaid diagram:', error);
          containerRef.current.innerHTML = `<div class="${styles.error}">Error rendering diagram: ${error}</div>`;
        }
      }
    };

    renderDiagram();
  }, [chart]);

  return (
    <div className={styles.container}>
      {title && <h4 className={styles.title}>{title}</h4>}
      <div
        ref={containerRef}
        className={styles.diagram}
        aria-label={alt}
      />
    </div>
  );
};

export default MermaidDiagram;