"""Video generation and composition service."""

import asyncio
import os
from pathlib import Path
from typing import Optional
import time

from script_to_film.models.script import Script, ScriptScene
from script_to_film.models.video import Video, VideoScene, VideoStatus
from script_to_film.config.settings import settings


class VideoGenerator:
    """Service for generating videos from scripts using Runway Gen-3."""

    def __init__(self, output_dir: str = "data/output") -> None:
        """
        Initialize the video generator.

        Args:
            output_dir: Directory for output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.runwayml_api_secret = settings.runwayml_api_secret

    async def generate_scene_video_runway(
        self, scene: ScriptScene, scene_number: int
    ) -> Optional[VideoScene]:
        """
        Generate video for a single scene using Runway Gen-3 API.
        Uses a two-step process: text-to-image, then image-to-video.

        Args:
            scene: Scene to generate video for
            scene_number: Scene number

        Returns:
            VideoScene with generated video path or None if failed
        """
        try:
            from runwayml import RunwayML

            # Initialize Runway client with API key
            client = RunwayML(api_key=self.runwayml_api_secret)

            # Determine duration based on scene (max 10 seconds for Gen-3)
            duration = min(int(scene.duration_seconds or 10), 10)

            print(f"Generating video for Scene {scene_number} with Runway Gen-3...")
            print(f"Prompt: {scene.video_prompt[:100]}...")

            # STEP 1: Generate an image from the text prompt
            print(f"Step 1: Generating image from prompt...")
            image_task = client.text_to_image.create(
                model='gen4_image',  # Use Gen-4 for image generation
                prompt_text=scene.video_prompt[:2048],  # Gen-4 supports longer prompts
                ratio="1920:1080",  # 16:9 aspect ratio in pixel dimensions
            )

            # Wait for image generation to complete
            image_task_id = image_task.id
            print(f"Image task created: {image_task_id}")

            max_wait = 120  # 2 minutes for image generation
            start_time = time.time()

            while time.time() - start_time < max_wait:
                await asyncio.sleep(5)  # Check every 5 seconds for image
                image_task = client.tasks.retrieve(image_task_id)
                print(f"Image task status: {image_task.status}")

                if image_task.status == 'SUCCEEDED':
                    break
                elif image_task.status == 'FAILED':
                    print(f"Image generation failed: {image_task.failure}")
                    return VideoScene(
                        scene_number=scene_number,
                        duration=duration,
                        status=VideoStatus.FAILED
                    )

            if image_task.status != 'SUCCEEDED':
                print(f"Image generation timed out")
                return VideoScene(
                    scene_number=scene_number,
                    duration=duration,
                    status=VideoStatus.FAILED
                )

            # Get the generated image URL
            image_url = image_task.output[0] if image_task.output else None
            if not image_url:
                print("No image URL in output")
                return VideoScene(
                    scene_number=scene_number,
                    duration=duration,
                    status=VideoStatus.FAILED
                )

            print(f"Image generated: {image_url}")

            # STEP 2: Create video from the generated image
            print(f"Step 2: Generating video from image...")
            task = client.image_to_video.create(
                model='gen3a_turbo',
                prompt_image=image_url,
                prompt_text=scene.video_prompt[:512],  # Max 512 characters for video prompt
                duration=duration,
                ratio="16:9",
                watermark=False
            )

            task_id = task.id
            print(f"Video task created: {task_id}")

            # Poll for completion (async)
            max_wait = 300  # 5 minutes max
            start_time = time.time()

            while time.time() - start_time < max_wait:
                await asyncio.sleep(10)  # Wait 10 seconds between checks

                task = client.tasks.retrieve(task_id)
                print(f"Task status: {task.status}")

                if task.status == 'SUCCEEDED':
                    # Download the video
                    video_url = task.output[0] if task.output else None

                    if video_url:
                        # Save video locally
                        video_filename = f"scene_{scene_number:03d}.mp4"
                        video_path = self.output_dir / video_filename

                        # Download video from URL
                        import httpx
                        async with httpx.AsyncClient() as http_client:
                            response = await http_client.get(video_url)
                            video_path.write_bytes(response.content)

                        print(f"Video saved: {video_path}")

                        return VideoScene(
                            scene_number=scene_number,
                            visual_path=str(video_path),
                            duration=duration,
                            status=VideoStatus.COMPLETED
                        )

                elif task.status == 'FAILED':
                    print(f"Task failed: {task.failure}")
                    return VideoScene(
                        scene_number=scene_number,
                        duration=duration,
                        status=VideoStatus.FAILED
                    )

            # Timeout
            print(f"Task timed out after {max_wait} seconds")
            return VideoScene(
                scene_number=scene_number,
                duration=duration,
                status=VideoStatus.FAILED
            )

        except Exception as e:
            print(f"Error generating video for scene {scene_number}: {e}")
            return VideoScene(
                scene_number=scene_number,
                duration=int(scene.duration_seconds or 10),
                status=VideoStatus.FAILED
            )

    async def generate_from_script(
        self, script: Script, resolution: str = "1920x1080", fps: int = 30, style: str = "realistic"
    ) -> Video:
        """
        Generate a video from a script using Runway Gen-3.

        Args:
            script: Script to convert to video
            resolution: Video resolution
            fps: Frames per second
            style: Visual style

        Returns:
            Video object with generation status
        """
        video = Video(
            script_id=script.id or "unknown",
            title=script.title,
            resolution=resolution,
            fps=fps,
            status=VideoStatus.PROCESSING,
        )

        try:
            # Generate videos for each scene using Runway Gen-3
            video_scenes = []
            for i, scene in enumerate(script.scenes):
                print(f"\nGenerating scene {i+1}/{len(script.scenes)}...")
                video_scene = await self.generate_scene_video_runway(scene, i)

                if video_scene:
                    video_scenes.append(video_scene)
                else:
                    print(f"Failed to generate scene {i}")

            video.scenes = video_scenes
            video.status = VideoStatus.COMPLETED if len(video_scenes) == len(script.scenes) else VideoStatus.FAILED
            video.duration = sum(scene.duration for scene in video_scenes)

            return video

        except Exception as e:
            print(f"Error generating video from script: {e}")
            video.status = VideoStatus.FAILED
            return video

    async def generate_scene_visuals(self, scene_number: int, prompt: str) -> str:
        """
        Generate visuals for a single scene.

        Args:
            scene_number: Scene number
            prompt: Visual generation prompt

        Returns:
            Path to generated visual file
        """
        # Placeholder - implement visual generation
        raise NotImplementedError("Scene visual generation not yet implemented")

    async def generate_scene_audio(
        self, scene_number: int, dialogue: list[dict[str, str]], duration: float
    ) -> str:
        """
        Generate audio for a single scene.

        Args:
            scene_number: Scene number
            dialogue: List of dialogue lines
            duration: Scene duration

        Returns:
            Path to generated audio file
        """
        # Placeholder - implement audio generation
        raise NotImplementedError("Scene audio generation not yet implemented")

    async def composite_scenes(
        self, scenes: list[VideoScene], output_path: str, resolution: str, fps: int
    ) -> str:
        """
        Composite all scenes into a final video.

        Args:
            scenes: List of video scenes
            output_path: Path for output video
            resolution: Video resolution
            fps: Frames per second

        Returns:
            Path to final video file
        """
        # Placeholder - implement video composition using moviepy or ffmpeg
        raise NotImplementedError("Video composition not yet implemented")

    async def generate_thumbnail(self, video_path: str, timestamp: float = 0.0) -> str:
        """
        Generate a thumbnail from a video.

        Args:
            video_path: Path to video file
            timestamp: Timestamp for thumbnail

        Returns:
            Path to thumbnail file
        """
        # Placeholder - implement thumbnail generation
        raise NotImplementedError("Thumbnail generation not yet implemented")
