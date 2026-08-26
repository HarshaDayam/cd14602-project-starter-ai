"""
Unit tests for the FlashcardLoader data validation.
"""

import pytest

from utils.flashcard_loader import FlashcardLoader, FlashcardValidationError


def test_load_valid_flashcards_array(tmp_path):
    """Verifies that flashcards in list format are loaded correctly."""
    file = tmp_path / "valid_array.json"
    file.write_text(
        '[{"front": "What is 1+1?", "back": "2"}, '
        '{"front": "What is 2+2?", "back": "4"}]',
        encoding="utf-8",
    )
    cards = FlashcardLoader.load_from_file(str(file))
    assert len(cards) == 2
    assert cards[0]["front"] == "What is 1+1?"
    assert cards[0]["back"] == "2"
    assert cards[1]["front"] == "What is 2+2?"
    assert cards[1]["back"] == "4"


def test_load_valid_flashcards_object(tmp_path):
    """Verifies that flashcards in wrapper object format are loaded
    correctly."""
    file = tmp_path / "valid_object.json"
    file.write_text(
        '{"cards": [{"front": "Q1", "back": "A1"}]}', encoding="utf-8"
    )
    cards = FlashcardLoader.load_from_file(str(file))
    assert len(cards) == 1
    assert cards[0]["front"] == "Q1"
    assert cards[0]["back"] == "A1"


def test_load_invalid_json(tmp_path):
    """Verifies that malformed JSON syntax raises an error."""
    file = tmp_path / "bad_syntax.json"
    file.write_text(
        '[{"front": "Q1", "back": "A1"',  # missing closing bracket/brace
        encoding="utf-8",
    )
    with pytest.raises(FlashcardValidationError) as excinfo:
        FlashcardLoader.load_from_file(str(file))
    assert "Invalid JSON syntax" in str(excinfo.value)


def test_load_missing_required_field(tmp_path):
    """Verifies that missing required fields (e.g. 'back') raise a
    validation error."""
    file = tmp_path / "missing_back.json"
    file.write_text('[{"front": "Only Front"}]', encoding="utf-8")
    with pytest.raises(FlashcardValidationError) as excinfo:
        FlashcardLoader.load_from_file(str(file))
    assert "missing the required 'back' field" in str(excinfo.value)


def test_load_nonexistent_file():
    """Verifies that FileNotFoundError is raised for missing files."""
    with pytest.raises(FileNotFoundError):
        FlashcardLoader.load_from_file("nonexistent_file.json")


def test_load_invalid_schema_types(tmp_path):
    """Verifies that non-string values raise a validation error."""
    file = tmp_path / "bad_types.json"
    file.write_text('[{"front": 123, "back": "A1"}]', encoding="utf-8")
    with pytest.raises(FlashcardValidationError) as excinfo:
        FlashcardLoader.load_from_file(str(file))
    assert "must be strings" in str(excinfo.value)


def test_load_empty_flashcard_list(tmp_path):
    """Verifies that empty flashcard datasets raise a validation error."""
    file_array = tmp_path / "empty_array.json"
    file_array.write_text("[]", encoding="utf-8")
    with pytest.raises(FlashcardValidationError) as excinfo:
        FlashcardLoader.load_from_file(str(file_array))
    assert "No flashcards found in the dataset" in str(excinfo.value)

    file_obj = tmp_path / "empty_object.json"
    file_obj.write_text('{"cards": []}', encoding="utf-8")
    with pytest.raises(FlashcardValidationError) as excinfo:
        FlashcardLoader.load_from_file(str(file_obj))
    assert "No flashcards found in the dataset" in str(excinfo.value)


def test_load_whitespace_only_fields(tmp_path):
    """Verifies that fields containing only spaces raise a validation error."""
    file = tmp_path / "whitespace.json"
    file.write_text('[{"front": "   ", "back": "A1"}]', encoding="utf-8")
    with pytest.raises(FlashcardValidationError) as excinfo:
        FlashcardLoader.load_from_file(str(file))
    assert "cannot be empty or only whitespace" in str(excinfo.value)
