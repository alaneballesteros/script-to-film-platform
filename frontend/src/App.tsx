import React, { useState } from 'react';
import Header from './components/Header';
import ScriptGenerator from './components/ScriptGenerator';
import ScriptDisplay from './components/ScriptDisplay';
import SceneBreakdown from './components/SceneBreakdown';
import VideoPrompts from './components/VideoPrompts';
import type { Script, ScriptScene } from './types';
import { FaArrowRight, FaCheckCircle } from 'react-icons/fa';

type Step = 'generate' | 'scenes' | 'prompts';

function App() {
  const [currentStep, setCurrentStep] = useState<Step>('generate');
  const [script, setScript] = useState<Script | null>(null);

  const handleScriptGenerated = (generatedScript: any) => {
    setScript(generatedScript);
    // Don't auto-advance - let user continue prompting or manually proceed
  };

  const handleRefineScript = async (feedback: string) => {
    if (!script) return;

    try {
      const { scriptService } = await import('./services/api');

      // Create a refinement prompt that includes the current script and feedback
      const refinementPrompt = `Please refine the following script based on this feedback: "${feedback}"\n\nCurrent script:\n${script.content}\n\nProvide the complete refined script.`;

      // Only include duration_preference if it's within valid range (60-600 seconds)
      const requestData: any = {
        prompt: refinementPrompt,
      };

      if (script.total_duration && script.total_duration >= 60 && script.total_duration <= 600) {
        requestData.duration_preference = Math.round(script.total_duration);
      }

      const refinedScript = await scriptService.generateScript(requestData);

      setScript(refinedScript);
    } catch (error) {
      console.error('Error refining script:', error);
      alert('Failed to refine script. Please try again.');
    }
  };

  const handleAnalyzeScript = async () => {
    // Scenes are already parsed by the backend, just move to scenes view
    setCurrentStep('scenes');
  };

  const handleGeneratePrompts = () => {
    setCurrentStep('prompts');
  };

  const handleUpdatePrompt = (sceneIndex: number, newPrompt: string) => {
    if (!script) return;

    const updatedScenes = [...script.scenes];
    updatedScenes[sceneIndex] = {
      ...updatedScenes[sceneIndex],
      video_prompt: newPrompt,
    };

    setScript({
      ...script,
      scenes: updatedScenes,
    });
  };

  const handleStartOver = () => {
    setScript(null);
    setCurrentStep('generate');
  };

  const steps = [
    { id: 'generate', label: '1. Generate Script', active: currentStep === 'generate' },
    { id: 'scenes', label: '2. Scene Breakdown', active: currentStep === 'scenes' },
    { id: 'prompts', label: '3. Video Prompts', active: currentStep === 'prompts' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {steps.map((step, index) => (
              <React.Fragment key={step.id}>
                <div className="flex items-center">
                  <button
                    onClick={() => setCurrentStep(step.id as Step)}
                    disabled={!script && step.id !== 'generate'}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
                      step.active
                        ? 'bg-primary-600 text-white shadow-lg scale-105'
                        : steps.findIndex((s) => s.active) > index
                        ? 'bg-green-500 text-white hover:bg-green-600 cursor-pointer'
                        : script
                        ? 'bg-gray-200 text-gray-600 hover:bg-gray-300 cursor-pointer'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                    } ${!script && step.id !== 'generate' ? 'opacity-50' : ''}`}
                  >
                    {steps.findIndex((s) => s.active) > index && (
                      <FaCheckCircle className="text-white" />
                    )}
                    <span className="font-medium text-sm">{step.label}</span>
                  </button>
                </div>
                {index < steps.length - 1 && (
                  <FaArrowRight className="text-gray-400 mx-2" />
                )}
              </React.Fragment>
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="space-y-8">
          {currentStep === 'generate' && (
            <>
              <ScriptGenerator onScriptGenerated={handleScriptGenerated} />
              {script && (
                <>
                  <ScriptDisplay
                    script={script}
                    onAnalyze={handleAnalyzeScript}
                    onRefine={handleRefineScript}
                  />
                  <div className="text-center space-x-4">
                    <button
                      onClick={() => setCurrentStep('scenes')}
                      className="btn-primary"
                    >
                      Continue to Scene Breakdown →
                    </button>
                  </div>
                </>
              )}
            </>
          )}

          {(currentStep === 'scenes' || currentStep === 'prompts') && script && (
            <>
              <SceneBreakdown script={script} />
              {currentStep === 'scenes' && (
                <div className="text-center">
                  <button onClick={handleGeneratePrompts} className="btn-primary">
                    Continue to Video Prompts
                  </button>
                </div>
              )}
            </>
          )}

          {currentStep === 'prompts' && script && (
            <>
              <VideoPrompts script={script} onUpdatePrompt={handleUpdatePrompt} />
              <div className="text-center">
                <button onClick={handleStartOver} className="btn-secondary">
                  Start New Project
                </button>
              </div>
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-gray-600 text-sm">
          <p>Script to Film Platform - AI-Powered Short Film Creation</p>
          <p className="mt-2">
            Use the generated prompts with RunwayML, Pika Labs, Stable Video Diffusion, or any
            text-to-video service
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
