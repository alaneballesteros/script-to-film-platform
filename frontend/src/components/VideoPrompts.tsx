import React, { useState } from 'react';
import { FaVideo, FaCopy, FaCheck, FaDownload, FaEdit } from 'react-icons/fa';
import type { Script, ScriptScene } from '../types';

interface VideoPromptsProps {
  script: Script;
  onUpdatePrompt?: (sceneIndex: number, newPrompt: string) => void;
}

const VideoPrompts: React.FC<VideoPromptsProps> = ({ script, onUpdatePrompt }) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editedPrompt, setEditedPrompt] = useState('');

  const handleCopy = (prompt: string, index: number) => {
    navigator.clipboard.writeText(prompt);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const handleEdit = (scene: ScriptScene, index: number) => {
    setEditingIndex(index);
    setEditedPrompt(scene.video_prompt || '');
  };

  const handleSaveEdit = (index: number) => {
    if (onUpdatePrompt) {
      onUpdatePrompt(index, editedPrompt);
    }
    setEditingIndex(null);
  };

  const handleCancelEdit = () => {
    setEditingIndex(null);
    setEditedPrompt('');
  };

  const handleExportAll = () => {
    const allPrompts = script.scenes
      .map((scene, index) => {
        return `Scene ${scene.scene_number + 1}: ${scene.location} - ${scene.time_of_day}\n${
          scene.video_prompt || 'No prompt generated'
        }\n`;
      })
      .join('\n---\n\n');

    const blob = new Blob([allPrompts], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${script.title.replace(/\s+/g, '_')}_video_prompts.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <FaVideo className="text-primary-600 text-2xl" />
          <h2 className="text-2xl font-bold text-gray-900">Text-to-Video Prompts</h2>
        </div>
        <button
          onClick={handleExportAll}
          className="btn-secondary flex items-center space-x-2 text-sm"
        >
          <FaDownload />
          <span>Export All</span>
        </button>
      </div>

      <div className="mb-6 p-4 bg-green-50 rounded-lg border border-green-200">
        <p className="text-sm text-green-800">
          <strong>Ready for video generation!</strong> Copy these prompts and use them with your
          preferred text-to-video service (RunwayML, Pika, Stable Video, etc.)
        </p>
      </div>

      <div className="space-y-6">
        {script.scenes.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <FaVideo className="mx-auto text-4xl mb-4 opacity-30" />
            <p>No video prompts available yet</p>
          </div>
        ) : (
          script.scenes.map((scene: ScriptScene, index: number) => (
            <div
              key={index}
              className="border-2 border-gray-200 rounded-lg p-5 hover:border-primary-300 transition-colors bg-white"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="bg-gradient-to-br from-primary-500 to-primary-700 text-white font-bold rounded-lg px-3 py-2 text-sm">
                    Scene {scene.scene_number + 1}
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 text-lg">
                      {scene.location}
                    </h3>
                    <p className="text-sm text-gray-500">{scene.time_of_day}</p>
                  </div>
                </div>
                {scene.duration_seconds && (
                  <div className="bg-gray-100 px-3 py-1 rounded-full text-sm text-gray-700">
                    {scene.duration_seconds.toFixed(1)}s
                  </div>
                )}
              </div>

              {editingIndex === index ? (
                <div className="space-y-3">
                  <textarea
                    value={editedPrompt}
                    onChange={(e) => setEditedPrompt(e.target.value)}
                    className="input-field min-h-[120px] font-mono text-sm"
                    placeholder="Edit video prompt..."
                  />
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleSaveEdit(index)}
                      className="btn-primary text-sm"
                    >
                      Save
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="btn-secondary text-sm"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <>
                  <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-4 mb-3 border border-blue-200">
                    <p className="text-gray-800 leading-relaxed">
                      {scene.video_prompt || 'Generating prompt...'}
                    </p>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleCopy(scene.video_prompt || '', index)}
                      className="flex items-center space-x-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
                    >
                      {copiedIndex === index ? (
                        <>
                          <FaCheck />
                          <span>Copied!</span>
                        </>
                      ) : (
                        <>
                          <FaCopy />
                          <span>Copy Prompt</span>
                        </>
                      )}
                    </button>
                    <button
                      onClick={() => handleEdit(scene, index)}
                      className="flex items-center space-x-2 px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors text-sm"
                    >
                      <FaEdit />
                      <span>Edit</span>
                    </button>
                  </div>
                </>
              )}
            </div>
          ))
        )}
      </div>

      <div className="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
        <p className="text-sm text-yellow-800">
          <strong>Tip:</strong> You can edit any prompt to better match your vision. Use these with
          services like RunwayML Gen-2, Pika Labs, or Stable Video Diffusion for best results.
        </p>
      </div>
    </div>
  );
};

export default VideoPrompts;
