"""Script models."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ScriptScene(BaseModel):
    """A scene in a script."""

    scene_number: int = Field(..., description="Scene number in the script")
    location: str = Field(..., description="Scene location")
    time_of_day: str = Field(..., description="Time of day (DAY, NIGHT, etc.)")
    description: str = Field(..., description="Scene action/description")
    dialogue: list[dict[str, str]] = Field(
        default_factory=list, description="Dialogue lines with character names"
    )
    duration_seconds: Optional[float] = Field(None, description="Estimated duration in seconds")
    video_prompt: Optional[str] = Field(None, description="Text-to-video prompt for this scene")


class Script(BaseModel):
    """A complete script."""

    id: Optional[str] = Field(None, description="Unique script ID")
    title: str = Field(..., description="Script title")
    author: Optional[str] = Field(None, description="Script author")
    content: str = Field(..., description="Raw script content")
    scenes: list[ScriptScene] = Field(default_factory=list, description="Parsed scenes")
    total_duration: Optional[float] = Field(None, description="Total duration in seconds")
    status: str = Field(default="draft", description="Script status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Update timestamp")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": "script_123",
                "title": "A Short Film",
                "author": "John Doe",
                "content": "INT. COFFEE SHOP - DAY\n\nA young programmer sits at a table...",
                "scenes": [],
                "total_duration": 120.0,
                "status": "draft",
            }
        }


class ScriptCreateRequest(BaseModel):
    """Request to create a script from existing content."""

    title: str = Field(..., description="Script title")
    content: str = Field(..., description="Raw script content")
    author: Optional[str] = Field(None, description="Script author")


class ScriptGenerateRequest(BaseModel):
    """Request to generate a script from a prompt."""

    prompt: str = Field(..., description="Story prompt or idea")
    duration_preference: Optional[int] = Field(
        90, description="Preferred duration in seconds", ge=30, le=600
    )
    genre: Optional[str] = Field(None, description="Genre (e.g., drama, comedy, thriller)")
    tone: Optional[str] = Field(None, description="Tone (e.g., serious, lighthearted, dark)")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "prompt": "A touching story about two old friends reuniting at a coffee shop",
                "duration_preference": 90,
                "genre": "Drama",
                "tone": "Nostalgic",
            }
        }


class ScriptResponse(BaseModel):
    """Response with script metadata."""

    id: str = Field(..., description="Script ID")
    title: str = Field(..., description="Script title")
    author: Optional[str] = Field(None, description="Script author")
    status: str = Field(..., description="Script status")
    scene_count: int = Field(..., description="Number of scenes")
    total_duration: Optional[float] = Field(None, description="Total duration in seconds")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")
