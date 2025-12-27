import React from 'react';
import clsx from 'clsx';
import styles from './SimulationViewer.module.css';

interface Props {
  src?: string;
  title?: string;
  description?: string;
  width?: string;
  height?: string;
}

const SimulationViewer = ({
  src,
  title,
  description,
  width = '100%',
  height = '400px',
}: Props): React.ReactElement => {
  return (
    <div className={clsx('simulation-container', styles.container)}>
      {title && <h4 className={styles.title}>{title}</h4>}
      <div
        className={styles.simulationWrapper}
        style={{ width, height }}
      >
        {src ? (
          <iframe
            src={src}
            title={title || 'Simulation Viewer'}
            className={styles.simulationFrame}
            width="100%"
            height="100%"
            frameBorder="0"
            allowFullScreen
          />
        ) : (
          <div className={styles.placeholder}>
            <div className={styles.placeholderIcon}>▶️</div>
            <p>Simulation content would appear here</p>
            <p className={styles.placeholderText}>
              This is a placeholder for interactive simulation content.
              In a real implementation, this would display robotics simulations.
            </p>
          </div>
        )}
      </div>
      {description && (
        <div className={styles.description}>
          {description}
        </div>
      )}
    </div>
  );
};

export default SimulationViewer;