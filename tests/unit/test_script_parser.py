"""Unit tests for script parser."""

import pytest

from script_to_film.services.script_parser import ScriptParser


@pytest.fixture
def script_parser() -> ScriptParser:
    """Create a script parser instance."""
    return ScriptParser()


@pytest.fixture
def sample_script() -> str:
    """Sample script content for testing."""
    return """
INT. COFFEE SHOP - DAY

Sarah sits at a corner table, typing on her laptop.

SARAH
(to herself)
This deadline is impossible.

John enters and waves.

JOHN
Hey! Mind if I join you?

SARAH
Of course not! How have you been?

EXT. PARK - EVENING

The two walk through a scenic park at sunset.

JOHN
I've been thinking about that project we discussed.

SARAH
Really? I thought you'd moved on from that idea.
"""


def test_parser_initialization(script_parser: ScriptParser) -> None:
    """Test that the parser initializes correctly."""
    assert script_parser is not None
    assert script_parser.scene_pattern is not None


def test_parse_script(script_parser: ScriptParser, sample_script: str) -> None:
    """Test parsing a complete script."""
    script = script_parser.parse(
        script_content=sample_script, title="Test Script", author="Test Author"
    )

    assert script.title == "Test Script"
    assert script.author == "Test Author"
    assert script.content == sample_script
    assert len(script.scenes) == 2


def test_extract_scenes(script_parser: ScriptParser, sample_script: str) -> None:
    """Test scene extraction from script."""
    scenes = script_parser._extract_scenes(sample_script)

    assert len(scenes) == 2

    # Check first scene
    first_scene = scenes[0]
    assert first_scene.scene_number == 0
    assert "COFFEE SHOP" in first_scene.location
    assert first_scene.time_of_day == "DAY"
    assert len(first_scene.dialogue) >= 2

    # Check second scene
    second_scene = scenes[1]
    assert second_scene.scene_number == 1
    assert "PARK" in second_scene.location
    assert second_scene.time_of_day == "EVENING"


def test_scene_duration_estimation(script_parser: ScriptParser) -> None:
    """Test that scene duration is estimated."""
    simple_script = """
INT. ROOM - NIGHT

A person sits alone.

PERSON
Hello world.
"""
    script = script_parser.parse(simple_script, "Simple Script")

    assert len(script.scenes) == 1
    assert script.scenes[0].duration_seconds is not None
    assert script.scenes[0].duration_seconds > 0


def test_empty_script(script_parser: ScriptParser) -> None:
    """Test parsing an empty script."""
    script = script_parser.parse("", "Empty Script")

    assert script.title == "Empty Script"
    assert len(script.scenes) == 0
    assert script.total_duration is None
