"""AI service for generating visual and audio content."""

from typing import Optional

import anthropic

from script_to_film.config.settings import settings


class AIService:
    """Service for interacting with AI models to generate content."""

    def __init__(self) -> None:
        """Initialize the AI service."""
        self.openai_api_key = settings.openai_api_key
        self.anthropic_api_key = settings.anthropic_api_key

    async def generate_script(
        self,
        prompt: str,
        duration_preference: Optional[int] = None,
        genre: Optional[str] = None,
        tone: Optional[str] = None,
    ) -> str:
        """
        Generate a script from a prompt using AI.

        Args:
            prompt: User's script idea
            duration_preference: Target duration in seconds
            genre: Desired genre
            tone: Desired tone

        Returns:
            Generated script content
        """
        # Build the user prompt with all parameters
        user_prompt = f"Write a short film script based on this idea: {prompt}"
        if genre:
            user_prompt += f"\nGenre: {genre}"
        if tone:
            user_prompt += f"\nTone: {tone}"
        if duration_preference:
            user_prompt += f"\nTarget duration: approximately {duration_preference} seconds"

        user_prompt += (
            "\n\n=== CRITICAL REQUIREMENTS ==="
            "\n1. Create a script with AT LEAST 3-5 DISTINCT SCENES"
            "\n2. Each scene MUST have a different location and/or time period"
            "\n3. Each scene MUST start with a scene heading (INT./EXT. LOCATION - TIME)"
            "\n4. Tell a complete story arc across multiple scenes"
            "\n\nExample structure:"
            "\n- Scene 1: Opening/Setup (establish characters and situation)"
            "\n- Scene 2: Development/Conflict (story progresses, time/location changes)"
            "\n- Scene 3: Climax/Resolution (conclusion in different setting)"
            "\n- Additional scenes as needed for the story"
            "\n\nFormat the script in proper screenplay format with:"
            "\n- Scene headings (INT./EXT. LOCATION - TIME OF DAY)"
            "\n- Action lines"
            "\n- Character names in ALL CAPS before dialogue"
            "\n- Dialogue beneath character names"
            "\n\nEnsure the script tells a complete story with clear progression across multiple distinct scenes and locations. Keep it concise, cinematic, and appropriate for the target duration."
        )

        try:
            # Use Anthropic Claude API
            client = anthropic.Anthropic(api_key=self.anthropic_api_key)

            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=6000,
                system="You are a professional screenwriter. Generate short film scripts in proper screenplay format with scene headings (INT./EXT.), action lines, and dialogue. CRITICAL REQUIREMENT: Always create scripts with AT LEAST 3-5 DISTINCT SCENES with different locations or time periods. Each scene must have its own scene heading. Never create single-scene scripts. Keep it concise and cinematic.",
                messages=[{"role": "user", "content": user_prompt}],
            )

            # Extract the text content from the response
            script_content = message.content[0].text
            return script_content

        except Exception as e:
            # Fallback to mock script if API fails
            print(f"Error calling Anthropic API: {e}")
            return """INT. COFFEE SHOP - DAY

A young woman, SARAH, sits at a corner table, typing on her laptop.

SARAH
(to herself)
This deadline is impossible.

JOHN enters and waves.

JOHN
Hey! Mind if I join you?

SARAH
Of course not! How have you been?

They sit and talk about their shared project.

EXT. PARK - EVENING

The two walk through a scenic park at sunset, the sky painted orange and pink.

JOHN
I've been thinking about that idea we discussed.

SARAH
Really? I thought you'd moved on from it.

JOHN
Never. Some ideas are worth pursuing.

Sarah smiles, inspired by his determination.

INT. SARAH'S APARTMENT - NIGHT

Sarah sits at her desk, working late. She looks at a photo of her and John from the park. Motivated, she types furiously, bringing their idea to life.

FADE OUT."""

    async def generate_scene_prompt(
        self, location: str, time_of_day: str, description: str, style: str = "realistic"
    ) -> str:
        """
        Generate a detailed prompt for visual generation.

        Args:
            location: Scene location
            time_of_day: Time of day for the scene
            description: Scene description
            style: Visual style (realistic, animated, etc.)

        Returns:
            Detailed prompt for image/video generation
        """
        prompt = (
            f"A {style} scene set in {location} during {time_of_day}. "
            f"{description}. High quality, cinematic lighting, professional film production."
        )
        return prompt

    async def generate_image(self, prompt: str, size: str = "1920x1080") -> bytes:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image
            size: Image size

        Returns:
            Image data as bytes
        """
        # Placeholder - implement with DALL-E, Stable Diffusion, or other model
        raise NotImplementedError("Image generation not yet implemented")

    async def generate_video(self, prompt: str, duration: float = 5.0) -> bytes:
        """
        Generate a video clip from a text prompt.

        Args:
            prompt: Text description of the video
            duration: Duration in seconds

        Returns:
            Video data as bytes
        """
        # Placeholder - implement with RunwayML, Pika, or other video generation model
        raise NotImplementedError("Video generation not yet implemented")

    async def generate_audio(
        self, text: str, voice: str = "default", emotion: Optional[str] = None
    ) -> bytes:
        """
        Generate audio/speech from text.

        Args:
            text: Text to convert to speech
            voice: Voice to use
            emotion: Emotional tone

        Returns:
            Audio data as bytes
        """
        # Placeholder - implement with ElevenLabs, OpenAI TTS, or other model
        raise NotImplementedError("Audio generation not yet implemented")

    async def generate_music(
        self, description: str, duration: float = 10.0, genre: Optional[str] = None
    ) -> bytes:
        """
        Generate background music.

        Args:
            description: Description of the desired music
            duration: Duration in seconds
            genre: Music genre

        Returns:
            Audio data as bytes
        """
        # Placeholder - implement with MusicGen, Suno, or other music generation model
        raise NotImplementedError("Music generation not yet implemented")
