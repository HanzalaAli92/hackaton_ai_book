import React, { useEffect } from 'react';

interface TextSelectionHandlerProps {
  onTextSelected: (selectedText: string) => void;
}

const TextSelectionHandler: React.FC<TextSelectionHandlerProps> = ({ onTextSelected }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection()?.toString().trim();
      if (selectedText && selectedText.length > 0) {
        // Only trigger if the selection is substantial (more than 5 characters)
        if (selectedText.length > 5) {
          onTextSelected(selectedText);
        }
      }
    };

    // Add event listeners for mouseup and keyup to detect text selection
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);

    // Clean up event listeners on component unmount
    return () => {
      document.removeEventListener('mouseup', handleSelection);
      document.removeEventListener('keyup', handleSelection);
    };
  }, [onTextSelected]);

  return null; // This component doesn't render anything itself
};

export default TextSelectionHandler;