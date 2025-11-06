import React, { useState } from 'react';
import { FaMagic, FaSpinner } from 'react-icons/fa';

interface ScriptGeneratorProps {
  onScriptGenerated: (script: any) => void;
}

const ScriptGenerator: React.FC<ScriptGeneratorProps> = ({ onScriptGenerated }) => {
  const [prompt, setPrompt] = useState('');
  const [genre, setGenre] = useState('');
  const [tone, setTone] = useState('');
  const [duration, setDuration] = useState<number>(120);  // 2 minutes default for multi-scene scripts
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      alert('Please enter a script idea');
      return;
    }

    setIsGenerating(true);

    try {
      // Call the actual API
      const { scriptService } = await import('../services/api');
      const script = await scriptService.generateScript({
        prompt,
        duration_preference: duration,
        genre: genre || undefined,
        tone: tone || undefined,
      });

      onScriptGenerated(script);
    } catch (error) {
      console.error('Error generating script:', error);
      alert('Failed to generate script. Please try again. Error: ' + (error as any).message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center space-x-3 mb-6">
        <FaMagic className="text-primary-600 text-2xl" />
        <h2 className="text-2xl font-bold text-gray-900">Generate Script from Idea</h2>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Script Idea / Prompt
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Describe your short film idea... (e.g., 'A heartwarming story about two friends reuniting after years apart')"
            className="input-field min-h-[120px] resize-none"
            disabled={isGenerating}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Genre (Optional)
            </label>
            <input
              type="text"
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              placeholder="e.g., Drama, Comedy"
              className="input-field"
              disabled={isGenerating}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tone (Optional)
            </label>
            <input
              type="text"
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              placeholder="e.g., Light, Dark, Inspirational"
              className="input-field"
              disabled={isGenerating}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Duration (seconds)
            </label>
            <input
              type="number"
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              min={60}
              max={600}
              step={30}
              className="input-field"
              disabled={isGenerating}
            />
            <p className="text-xs text-gray-500 mt-1">1-10 minutes (60-600 seconds)</p>
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={isGenerating || !prompt.trim()}
          className="btn-primary w-full flex items-center justify-center space-x-2"
        >
          {isGenerating ? (
            <>
              <FaSpinner className="animate-spin" />
              <span>Generating Script...</span>
            </>
          ) : (
            <>
              <FaMagic />
              <span>Generate Script</span>
            </>
          )}
        </button>
      </div>

      <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-sm text-blue-800">
          <strong>Tip:</strong> Be specific about the story, characters, and setting. The AI will create a complete screenplay with at least 3 distinct scenes, each optimized for video generation.
        </p>
      </div>
    </div>
  );
};

export default ScriptGenerator;
