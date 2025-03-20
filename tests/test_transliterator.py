from pathlib import Path

import pytest
import yaml

from src.hindi_transliteration import HindiTransliterator


@pytest.fixture
def transcripts():
    """Load transcripts from YAML file."""
    test_data_path = Path(__file__).parent / "data" / "test_cases.yaml"
    with open(test_data_path, encoding="utf-8") as f:
        return yaml.safe_load(f)["transcripts"]


@pytest.fixture
def transliterator():
    """Create a transliterator instance."""
    return HindiTransliterator()


def normalize_text(text: str) -> str:
    """Normalize text by removing extra whitespace and normalizing line endings."""
    return "\n".join(line.strip() for line in text.strip().splitlines())


def test_transliteration_from_yaml(transliterator, transcripts):
    """Test transliteration using transcripts from YAML file."""
    for transcript in transcripts:
        result = transliterator.transliterate(transcript["input"])
        assert result.strip() == transcript["expected"].strip()


def test_specific_cases(transliterator):
    """Test specific edge cases and common patterns."""
    test_pairs = [
        ("ज़मीन", "zamin"),
        ("चाँद", "chaand"),
        ("क्षमा", "kshama"),
        ("लक्ष्मी", "lakshmi"),
        ("ज्ञान", "gyan"),
        ("पद्म", "padm"),
        ("१२३", "123"),
    ]

    for input_text, expected in test_pairs:
        assert (
            transliterator.transliterate(input_text) == expected
        ), f"Failed to transliterate: {input_text}"


def test_whitespace_handling(transliterator):
    """Test handling of various whitespace patterns."""
    assert transliterator.transliterate("राम  राम") == "raam  raam"
    assert transliterator.transliterate("राम\nराम") == "raam\nraam"
    assert transliterator.transliterate("राम\tराम") == "raam\traam"


def test_mixed_script(transliterator):
    """Test handling of mixed Devanagari and Latin text."""
    assert transliterator.transliterate("topic (विषय)") == "topic (vishay)"
