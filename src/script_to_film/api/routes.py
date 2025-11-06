"""API routes for the script-to-film platform."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from script_to_film.models.script import (
    Script,
    ScriptCreateRequest,
    ScriptGenerateRequest,
    ScriptResponse,
)
from script_to_film.models.video import (
    SceneVideoGenerateRequest,
    VideoGenerateRequest,
    VideoResponse,
    VideoScene,
    VideoStatus,
)
from script_to_film.services.ai_service import AIService
from script_to_film.services.script_parser import ScriptParser
from script_to_film.services.video_generator import VideoGenerator

router = APIRouter()
script_parser = ScriptParser()
video_generator = VideoGenerator()
ai_service = AIService()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Script to Film API", "version": "0.1.0"}


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


# Script endpoints
@router.post("/scripts", response_model=ScriptResponse, status_code=status.HTTP_201_CREATED)
async def create_script(request: ScriptCreateRequest) -> ScriptResponse:
    """
    Create a new script from text content.

    Args:
        request: Script creation request

    Returns:
        Created script response
    """
    # Parse the script
    script = script_parser.parse(
        script_content=request.content, title=request.title, author=request.author
    )

    # In production, save to database here
    script.id = "script_123"  # Placeholder

    return ScriptResponse(
        id=script.id,
        title=script.title,
        author=script.author,
        status=script.status,
        scene_count=len(script.scenes),
        total_duration=script.total_duration,
        created_at=script.created_at,
        updated_at=script.updated_at,
    )


@router.get("/scripts/{script_id}", response_model=ScriptResponse)
async def get_script(script_id: str) -> ScriptResponse:
    """
    Get a script by ID.

    Args:
        script_id: Script ID

    Returns:
        Script response
    """
    # In production, fetch from database
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Script not found")


@router.get("/scripts", response_model=List[ScriptResponse])
async def list_scripts(skip: int = 0, limit: int = 100) -> List[ScriptResponse]:
    """
    List all scripts.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of script responses
    """
    # In production, fetch from database
    return []


@router.post("/scripts/generate", response_model=Script, status_code=status.HTTP_201_CREATED)
async def generate_script(request: ScriptGenerateRequest) -> Script:
    """
    Generate a script from a prompt using AI.

    Args:
        request: Script generation request with prompt and preferences

    Returns:
        Generated and parsed script
    """
    # Generate script content using AI
    script_content = await ai_service.generate_script(
        prompt=request.prompt,
        duration_preference=request.duration_preference,
        genre=request.genre,
        tone=request.tone,
    )

    # Extract title from prompt (first few words)
    title = " ".join(request.prompt.split()[:5])
    if len(request.prompt.split()) > 5:
        title += "..."

    # Parse the generated script
    script = script_parser.parse(script_content=script_content, title=title, author="AI Generated")

    # Generate a unique ID
    import uuid

    script.id = f"script_{uuid.uuid4().hex[:12]}"

    # In production, save to database here

    return script


@router.post("/scripts/{script_id}/video-prompts", response_model=Script)
async def generate_video_prompts(script_id: str) -> Script:
    """
    Generate text-to-video prompts for all scenes in a script.

    Args:
        script_id: Script ID

    Returns:
        Script with video prompts added to each scene
    """
    # In production, fetch script from database
    # For now, return mock data
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Video prompt generation endpoint - fetch script from DB and generate prompts",
    )


# Video endpoints
@router.post("/videos", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def generate_video(request: VideoGenerateRequest) -> VideoResponse:
    """
    Generate a video from a script.

    Args:
        request: Video generation request

    Returns:
        Video generation response
    """
    # In production, fetch script from database and queue video generation task
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Video generation not yet implemented",
    )


@router.get("/videos/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str) -> VideoResponse:
    """
    Get a video by ID.

    Args:
        video_id: Video ID

    Returns:
        Video response
    """
    # In production, fetch from database
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")


@router.get("/videos", response_model=List[VideoResponse])
async def list_videos(skip: int = 0, limit: int = 100) -> List[VideoResponse]:
    """
    List all videos.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of video responses
    """
    # In production, fetch from database
    return []


@router.post("/videos/scene", response_model=VideoScene, status_code=status.HTTP_201_CREATED)
async def generate_scene_video(request: SceneVideoGenerateRequest) -> VideoScene:
    """
    Generate video for a single scene using Runway Gen-3.

    Args:
        request: Scene video generation request

    Returns:
        VideoScene with generation status and video path
    """
    from script_to_film.models.script import ScriptScene

    # Convert request to ScriptScene
    scene = ScriptScene(
        scene_number=request.scene_number,
        location=request.location or "Unknown",
        time_of_day=request.time_of_day or "DAY",
        description="",
        dialogue=[],
        duration_seconds=request.duration_seconds,
        video_prompt=request.video_prompt,
    )

    # Generate video using Runway Gen-3
    video_scene = await video_generator.generate_scene_video_runway(scene, request.scene_number)

    if video_scene is None or video_scene.status == VideoStatus.FAILED:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate video for scene. Check backend logs for details.",
        )

    return video_scene
