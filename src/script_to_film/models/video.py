"""Video models."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class VideoStatus(str, Enum):
    """Video generation status."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoScene(BaseModel):
    """A scene in a video."""

    scene_number: int = Field(..., description="Scene number")
    visual_path: Optional[str] = Field(None, description="Path to visual file")
    audio_path: Optional[str] = Field(None, description="Path to audio file")
    duration: float = Field(..., description="Scene duration in seconds")
    status: VideoStatus = Field(VideoStatus.PENDING, description="Scene generation status")


class Video(BaseModel):
    """A generated video."""

    id: Optional[str] = Field(None, description="Video ID")
    script_id: str = Field(..., description="Associated script ID")
    title: str = Field(..., description="Video title")
    scenes: list[VideoScene] = Field(default_factory=list, description="Video scenes")
    resolution: str = Field(..., description="Video resolution")
    fps: int = Field(..., description="Frames per second")
    status: VideoStatus = Field(VideoStatus.PENDING, description="Video generation status")
    output_path: Optional[str] = Field(None, description="Path to final video file")
    thumbnail_path: Optional[str] = Field(None, description="Path to thumbnail file")
    duration: Optional[float] = Field(None, description="Total duration in seconds")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Update timestamp")


class VideoGenerateRequest(BaseModel):
    """Request to generate a video from a script."""

    script_id: str = Field(..., description="Script ID to generate video from")
    style: Optional[str] = Field("realistic", description="Visual style (realistic, animated, etc.)")
    resolution: Optional[str] = Field("1920x1080", description="Video resolution")
    fps: Optional[int] = Field(30, description="Frames per second")


class SceneVideoGenerateRequest(BaseModel):
    """Request to generate video for a single scene."""

    video_prompt: str = Field(..., description="Text-to-video prompt for the scene")
    duration_seconds: float = Field(..., description="Scene duration in seconds (will be clamped to 5-10 range)")
    scene_number: int = Field(..., description="Scene number")
    location: Optional[str] = Field(None, description="Scene location")
    time_of_day: Optional[str] = Field(None, description="Time of day")


class VideoResponse(BaseModel):
    """Response with video metadata."""

    id: str = Field(..., description="Video ID")
    script_id: str = Field(..., description="Associated script ID")
    status: str = Field(..., description="Video generation status")
    url: Optional[str] = Field(None, description="Video URL if completed")
    duration: Optional[float] = Field(None, description="Video duration in seconds")
    resolution: str = Field(..., description="Video resolution")
    fps: int = Field(..., description="Frames per second")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
