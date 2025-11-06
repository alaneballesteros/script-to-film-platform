"""Script parsing service."""

import re
from typing import Optional

from script_to_film.models.script import Script, ScriptScene


class ScriptParser:
    """Parser for converting raw script text into structured scenes."""

    def __init__(self) -> None:
        """Initialize the script parser."""
        self.scene_pattern = re.compile(
            r"(?:INT\.|EXT\.)\s+(.+?)\s+-\s+(DAY|NIGHT|MORNING|EVENING)", re.IGNORECASE
        )

    def parse(self, script_content: str, title: str, author: Optional[str] = None) -> Script:
        """
        Parse a script from text content.

        Args:
            script_content: Raw script text
            title: Script title
            author: Script author

        Returns:
            Parsed Script object with structured scenes
        """
        scenes = self._extract_scenes(script_content)
        total_duration = sum(scene.duration_seconds or 0 for scene in scenes)

        return Script(
            title=title,
            author=author,
            content=script_content,
            scenes=scenes,
            total_duration=total_duration if total_duration > 0 else None,
        )

    def _extract_scenes(self, content: str) -> list[ScriptScene]:
        """Extract scenes from script content."""
        scenes = []
        lines = content.split("\n")
        current_scene: Optional[dict] = None
        scene_number = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for scene heading
            scene_match = self.scene_pattern.match(line)
            if scene_match:
                # Save previous scene if exists
                if current_scene:
                    scenes.append(self._create_scene(scene_number, current_scene))
                    scene_number += 1

                # Start new scene
                current_scene = {
                    "location": scene_match.group(1).strip(),
                    "time_of_day": scene_match.group(2).strip(),
                    "description": "",
                    "dialogue": [],
                }
            elif current_scene:
                # Add content to current scene
                if line.isupper() and len(line.split()) <= 3:
                    # Character name
                    current_scene["current_character"] = line
                elif current_scene.get("current_character"):
                    # Dialogue
                    current_scene["dialogue"].append(
                        {"character": current_scene["current_character"], "line": line}
                    )
                    current_scene["current_character"] = None
                else:
                    # Action/description
                    current_scene["description"] += f" {line}"

        # Save last scene
        if current_scene:
            scenes.append(self._create_scene(scene_number, current_scene))

        return scenes

    def _create_scene(self, scene_number: int, scene_data: dict) -> ScriptScene:
        """Create a ScriptScene object from parsed data."""
        # Estimate duration based on dialogue and description length
        dialogue_duration = len(scene_data["dialogue"]) * 3  # ~3 seconds per dialogue line
        description_words = len(scene_data["description"].split())
        description_duration = description_words * 0.3  # ~0.3 seconds per word

        # Generate video prompt for the scene
        location = scene_data["location"]
        time_of_day = scene_data["time_of_day"]
        description = scene_data["description"].strip()

        # Determine lighting and atmosphere based on time of day
        lighting = ""
        if "DAY" in time_of_day.upper():
            lighting = "natural daylight, bright and clear"
        elif "NIGHT" in time_of_day.upper():
            lighting = "low-key lighting, atmospheric shadows, cinematic night"
        elif "MORNING" in time_of_day.upper():
            lighting = "soft morning light, golden hour"
        elif "EVENING" in time_of_day.upper() or "DUSK" in time_of_day.upper():
            lighting = "warm golden hour lighting, sunset glow"
        else:
            lighting = "cinematic lighting"

        # Determine interior/exterior
        int_ext = "Interior" if "INT" in location else "Exterior"

        # Build the video prompt
        video_prompt = (
            f"{int_ext} of {location.lower()} during {time_of_day.lower()}, "
            f"{lighting}. {description} "
            f"Cinematic composition, professional film quality, 4K, realistic."
        )

        return ScriptScene(
            scene_number=scene_number,
            location=scene_data["location"],
            time_of_day=scene_data["time_of_day"],
            description=scene_data["description"].strip(),
            dialogue=scene_data["dialogue"],
            duration_seconds=max(dialogue_duration + description_duration, 5.0),
            video_prompt=video_prompt,
        )
