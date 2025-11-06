import React from 'react';
import { FaLayerGroup, FaClock, FaMapMarkerAlt, FaSun, FaMoon } from 'react-icons/fa';
import type { Script, ScriptScene } from '../types';

interface SceneBreakdownProps {
  script: Script;
}

const SceneBreakdown: React.FC<SceneBreakdownProps> = ({ script }) => {
  const getTimeIcon = (timeOfDay: string) => {
    const time = timeOfDay.toLowerCase();
    if (time.includes('day') || time.includes('morning')) {
      return <FaSun className="text-yellow-500" />;
    }
    return <FaMoon className="text-indigo-500" />;
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A';
    return `${seconds.toFixed(1)}s`;
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <FaLayerGroup className="text-primary-600 text-2xl" />
          <h2 className="text-2xl font-bold text-gray-900">Scene Breakdown</h2>
        </div>
        <div className="text-sm text-gray-600">
          <span className="font-semibold">{script.scenes.length}</span> scenes
          {script.total_duration && (
            <span className="ml-2">
              • <FaClock className="inline" /> {formatDuration(script.total_duration)} total
            </span>
          )}
        </div>
      </div>

      <div className="space-y-4">
        {script.scenes.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <FaLayerGroup className="mx-auto text-4xl mb-4 opacity-30" />
            <p>No scenes parsed yet</p>
          </div>
        ) : (
          script.scenes.map((scene: ScriptScene, index: number) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center space-x-3">
                  <div className="bg-primary-100 text-primary-700 font-bold rounded-full w-10 h-10 flex items-center justify-center">
                    {scene.scene_number + 1}
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <FaMapMarkerAlt className="text-gray-400 text-sm" />
                      <h3 className="font-semibold text-gray-900">{scene.location}</h3>
                    </div>
                    <div className="flex items-center space-x-2 mt-1">
                      {getTimeIcon(scene.time_of_day)}
                      <span className="text-sm text-gray-600">{scene.time_of_day}</span>
                    </div>
                  </div>
                </div>
                {scene.duration_seconds && (
                  <div className="flex items-center space-x-1 text-gray-600 text-sm">
                    <FaClock />
                    <span>{formatDuration(scene.duration_seconds)}</span>
                  </div>
                )}
              </div>

              {scene.description && (
                <div className="mb-3">
                  <p className="text-gray-700 text-sm bg-gray-50 p-3 rounded">
                    {scene.description}
                  </p>
                </div>
              )}

              {scene.dialogue && scene.dialogue.length > 0 && (
                <div className="space-y-2">
                  <p className="text-xs font-semibold text-gray-500 uppercase">Dialogue</p>
                  {scene.dialogue.map((line, lineIndex) => (
                    <div key={lineIndex} className="pl-4 border-l-2 border-primary-200">
                      <p className="font-semibold text-sm text-gray-900">{line.character}</p>
                      <p className="text-sm text-gray-700">{line.line}</p>
                    </div>
                  ))}
                </div>
              )}

              {scene.video_prompt && (
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-xs font-semibold text-primary-600 uppercase mb-1">
                    Video Prompt
                  </p>
                  <p className="text-sm text-gray-700 bg-primary-50 p-3 rounded">
                    {scene.video_prompt}
                  </p>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SceneBreakdown;
