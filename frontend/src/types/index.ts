export interface ScriptScene {
  scene_number: number;
  location: string;
  time_of_day: string;
  description: string;
  dialogue: Array<{
    character: string;
    line: string;
  }>;
  duration_seconds?: number;
  video_prompt?: string;
}

export interface Script {
  id?: string;
  title: string;
  author?: string;
  content: string;
  scenes: ScriptScene[];
  total_duration?: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  created_at?: string;
  updated_at?: string;
}

export interface ScriptCreateRequest {
  title: string;
  author?: string;
  content: string;
}

export interface ScriptGenerateRequest {
  prompt: string;
  duration_preference?: number;
  genre?: string;
  tone?: string;
}

export interface ScriptResponse {
  id: string;
  title: string;
  author?: string;
  status: string;
  scene_count: number;
  total_duration?: number;
  created_at: string;
  updated_at: string;
}

export interface VideoPrompt {
  scene_number: number;
  prompt: string;
  duration: number;
  style_guidance?: string;
}
