import React, { useState } from 'react';
import { FaFileAlt, FaCopy, FaDownload, FaComment, FaPaperPlane } from 'react-icons/fa';
import type { Script } from '../types';

interface ScriptDisplayProps {
  script: Script;
  onAnalyze: () => void;
  onRefine?: (feedback: string) => void;
}

const ScriptDisplay: React.FC<ScriptDisplayProps> = ({ script, onAnalyze, onRefine }) => {
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [isRefining, setIsRefining] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(script.content);
    alert('Script copied to clipboard!');
  };

  const handleDownload = () => {
    const blob = new Blob([script.content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${script.title.replace(/\s+/g, '_')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleSubmitFeedback = async () => {
    if (!feedback.trim() || !onRefine) return;

    setIsRefining(true);
    try {
      await onRefine(feedback);
      setFeedback('');
      setShowFeedback(false);
    } catch (error) {
      console.error('Error refining script:', error);
    } finally {
      setIsRefining(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <FaFileAlt className="text-primary-600 text-2xl" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{script.title}</h2>
            {script.author && (
              <p className="text-sm text-gray-500">by {script.author}</p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopy}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all"
            title="Copy to clipboard"
          >
            <FaCopy />
          </button>
          <button
            onClick={handleDownload}
            className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-all"
            title="Download script"
          >
            <FaDownload />
          </button>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-6 border border-gray-200 max-h-96 overflow-y-auto">
        <pre className="whitespace-pre-wrap font-mono text-sm text-gray-800">
          {script.content}
        </pre>
      </div>

      {script.scenes && script.scenes.length > 0 && (
        <div className="mt-4 p-4 bg-green-50 rounded-lg border border-green-200">
          <p className="text-sm text-green-800">
            <strong>✓ Script parsed:</strong> {script.scenes.length} scenes detected with video prompts ready!
          </p>
        </div>
      )}

      {/* Feedback Section */}
      <div className="mt-6 border-t pt-6">
        {!showFeedback ? (
          <button
            onClick={() => setShowFeedback(true)}
            className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors w-full justify-center"
          >
            <FaComment />
            <span>Give Feedback to Refine Script</span>
          </button>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-gray-900 flex items-center space-x-2">
                <FaComment className="text-blue-600" />
                <span>Refine Your Script</span>
              </h3>
              <button
                onClick={() => setShowFeedback(false)}
                className="text-gray-500 hover:text-gray-700 text-sm"
              >
                Cancel
              </button>
            </div>
            <textarea
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              placeholder="Provide feedback to refine the script (e.g., 'Make it more dramatic', 'Add more dialogue', 'Change the ending to be happier')"
              className="input-field min-h-[100px] resize-none"
              disabled={isRefining}
            />
            <button
              onClick={handleSubmitFeedback}
              disabled={!feedback.trim() || isRefining}
              className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
            >
              {isRefining ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Refining Script...</span>
                </>
              ) : (
                <>
                  <FaPaperPlane />
                  <span>Apply Feedback</span>
                </>
              )}
            </button>
            <p className="text-xs text-gray-500">
              The AI will adjust the current script based on your feedback while maintaining the overall structure.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScriptDisplay;
