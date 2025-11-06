# Runway Gen-3 API Integration Guide

## Overview

The Script-to-Film platform now integrates with **Runway Gen-3 Alpha Turbo** to automatically generate professional videos from script scenes.

## What's Integrated

✅ **Runway Gen-3 Alpha Turbo API**
- Text-to-video generation for each scene
- Optimized prompts following Runway's best practices
- Automatic video downloading and storage
- Async processing with status polling

## Setup Instructions

### 1. Get Your Runway API Key

1. Go to [https://runwayml.com](https://runwayml.com)
2. Sign up or log in to your account
3. Navigate to **Settings** → **API Keys**
4. Create a new API key
5. **IMPORTANT:** Copy the key immediately (it's only shown once)

### 2. Configure Environment Variable

Add your Runway API key to the `.env` file:

```bash
RUNWAYML_API_SECRET=your_runway_api_key_here
```

### 3. Install Dependencies

The `runwayml` package is already in `requirements.txt`. If you need to reinstall:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## How It Works

### 1. Script Generation
User provides a prompt → Claude Sonnet 4.5 generates screenplay

### 2. Scene Breakdown
Script is parsed into scenes with:
- Location and time of day
- Character actions and dialogue
- Estimated duration

### 3. Prompt Optimization
Each scene gets a professional video prompt:
```
[Camera Angle]: [Scene Description]. [Lighting]. [Environment Details].
Cinematic composition, 4K resolution, film grain, shallow depth of field.
```

Example:
```
Medium shot: Interior of coffee shop during day. A young programmer sits at
a corner table typing on laptop. Natural daylight, bright and clear, high
contrast. Realistic indoor environment, detailed set design, depth of field.
Cinematic composition, professional film quality, 4K resolution, realistic
textures and materials, subtle camera movement, film grain, shallow depth
of field.
```

### 4. Video Generation (NEW!)
For each scene:
1. API request sent to Runway Gen-3 with optimized prompt
2. Task ID returned immediately
3. System polls every 10 seconds for completion
4. Video downloaded and saved to `data/output/scene_XXX.mp4`
5. All scene videos available for final compilation

## API Endpoints

### Generate Video from Script

**Endpoint:** `POST /api/v1/videos`

**Request:**
```json
{
  "script_id": "script_abc123",
  "style": "realistic",
  "resolution": "1920x1080",
  "fps": 30
}
```

**Response:**
```json
{
  "id": "video_xyz789",
  "script_id": "script_abc123",
  "status": "processing",
  "scenes": [
    {
      "scene_number": 0,
      "visual_path": null,
      "duration": 10.0,
      "status": "pending"
    }
  ],
  "resolution": "1920x1080",
  "fps": 30,
  "created_at": "2025-11-06T00:00:00Z"
}
```

## Video Generation Specifications

### Runway Gen-3 Alpha Turbo

**Duration:**
- Minimum: 5 seconds
- Maximum: 10 seconds
- Default: 10 seconds

**Resolution:**
- Ratio: 16:9 (recommended)
- Output: 1280x768 (upscalable)

**Prompt Limits:**
- Max characters: 512
- Automatically truncated if longer

**Cost:**
- 5 seconds: $0.25
- 10 seconds: $0.50

**Generation Time:**
- Typically: 30-90 seconds per scene
- Max wait: 5 minutes (then timeout)

## Features

### Automatic Scene Processing
- **Parallel Processing:** Scenes can be processed concurrently (future enhancement)
- **Progress Tracking:** Real-time status updates
- **Error Handling:** Graceful fallbacks if generation fails
- **Retry Logic:** Automatic retries on transient failures

### Video Management
- **Local Storage:** Videos saved to `data/output/`
- **Naming Convention:** `scene_001.mp4`, `scene_002.mp4`, etc.
- **Format:** MP4 (H.264)
- **Quality:** 4K-ready, professional grade

### Prompt Optimization
- **Camera Variety:** Different angles per scene (medium, wide, close-up, etc.)
- **Lighting Control:** Time-of-day appropriate lighting
- **Cinematic Quality:** Film grain, depth of field, professional composition
- **Environment Details:** Interior vs exterior specific optimizations

## Usage Example

### Python Code

```python
from script_to_film.services.video_generator import VideoGenerator
from script_to_film.services.script_parser import ScriptParser

# Parse a script
parser = ScriptParser()
script = parser.parse(
    script_content=your_script_text,
    title="My Short Film"
)

# Generate videos for all scenes
generator = VideoGenerator()
video = await generator.generate_from_script(script)

print(f"Generated {len(video.scenes)} scene videos")
print(f"Total duration: {video.duration} seconds")
print(f"Status: {video.status}")

# Access individual scene videos
for scene in video.scenes:
    if scene.visual_path:
        print(f"Scene {scene.scene_number}: {scene.visual_path}")
```

### API Call

```bash
# 1. Generate script
curl -X POST http://localhost:8000/api/v1/scripts/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A touching story about two old friends reuniting",
    "duration_preference": 60,
    "genre": "Drama"
  }'

# 2. Generate videos from script
curl -X POST http://localhost:8000/api/v1/videos \
  -H "Content-Type: application/json" \
  -d '{
    "script_id": "script_abc123"
  }'
```

## Technical Details

### Async Processing
```python
async def generate_scene_video_runway(scene, scene_number):
    # Initialize Runway client
    client = RunwayML(api_key=settings.runwayml_api_secret)

    # Create generation task
    task = client.image_to_video.create(
        model='gen3a_turbo',
        prompt_text=scene.video_prompt[:512],
        duration=min(int(scene.duration_seconds), 10),
        ratio="16:9",
        watermark=False
    )

    # Poll for completion
    while task.status not in ['SUCCEEDED', 'FAILED']:
        await asyncio.sleep(10)
        task = client.tasks.retrieve(task.id)

    # Download video
    if task.status == 'SUCCEEDED':
        video_url = task.output[0]
        # Save video locally
        ...
```

### Camera Angles
The system rotates through 8 camera angles:
1. Medium shot
2. Wide angle establishing shot
3. Close-up shot
4. Low angle shot
5. Over-the-shoulder shot
6. Dutch angle shot
7. High angle shot
8. Tracking shot

This creates visual variety across scenes.

## Limitations & Future Enhancements

### Current Limitations
- ⏱️ 10-second max per scene (Runway Gen-3 limit)
- 🔄 Sequential processing (one scene at a time)
- 💰 Cost accumulates per scene
- 🎬 No automatic video stitching yet

### Planned Enhancements
- [ ] Parallel scene processing for faster generation
- [ ] Automatic video compilation (stitch all scenes)
- [ ] Audio generation and sync (dialogue, music, SFX)
- [ ] Alternative providers (Luma, Google Veo 3)
- [ ] Background processing with webhooks
- [ ] Progress bar in frontend
- [ ] Video preview before final render
- [ ] Custom camera control per scene
- [ ] Cost estimation before generation
- [ ] Batch processing for multiple scripts

## Troubleshooting

### API Key Not Working
**Error:** `Authentication failed`
**Solution:** Verify your API key in `.env` file:
```bash
echo $RUNWAYML_API_SECRET
```

### Task Timeout
**Error:** `Task timed out after 300 seconds`
**Solution:** This is normal for complex scenes. The video should still be accessible in your Runway dashboard.

### Generation Failed
**Error:** `Task failed: [error message]`
**Common causes:**
- Prompt violates content policy
- Prompt too vague
- Service temporarily unavailable

**Solution:** Check prompt content and try again.

### No Video URL
**Error:** `video_url is None`
**Solution:** Task may have succeeded but output not available. Check Runway dashboard or retry.

## Cost Management

### Estimating Costs

```python
def estimate_cost(script):
    scenes = len(script.scenes)
    avg_duration = sum(s.duration_seconds for s in script.scenes) / scenes

    cost_per_scene = 0.50 if avg_duration > 5 else 0.25
    total_cost = scenes * cost_per_scene

    print(f"Estimated cost: ${total_cost:.2f}")
    print(f"({scenes} scenes × ${cost_per_scene})")
```

### Tips to Reduce Costs
1. **Shorten scenes:** Keep under 5 seconds when possible
2. **Fewer scenes:** Consolidate similar scenes
3. **Test first:** Generate 1-2 scenes before full script
4. **Use preview:** Check scene breakdown before generating videos

## Best Practices

### Prompt Writing
✅ **Do:**
- Be specific about camera angles
- Describe lighting conditions
- Include environmental details
- Mention specific actions
- Add quality descriptors (4K, cinematic, etc.)

❌ **Don't:**
- Use negative phrasing ("don't move")
- Be too vague ("nice scene")
- Exceed 512 characters
- Include copyrighted characters

### Scene Planning
- Keep scenes under 10 seconds
- Plan for 5-8 scenes per short film
- Consider shot variety
- Match lighting to time of day
- Think about transitions between scenes

## Support

For issues with:
- **Runway API:** [https://help.runwayml.com](https://help.runwayml.com)
- **Platform Integration:** Open an issue on GitHub

## Resources

- [Runway Gen-3 Documentation](https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide)
- [RunwayML Python SDK](https://github.com/Runway-Software/runway-python)
- [Text-to-Video Research](./TEXT_TO_VIDEO_RESEARCH.md)

---

**Last Updated:** November 2025
**API Version:** Runway Gen-3 Alpha Turbo
**Integration Status:** ✅ Active & Tested
