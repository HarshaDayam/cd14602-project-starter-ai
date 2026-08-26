"""
Utility module for loading and validating flashcard data from JSON files.
"""

import json
from pathlib import Path
from typing import Any, Dict, List


class FlashcardValidationError(Exception):
    """Custom exception raised when flashcard validation fails."""

    pass


class FlashcardLoader:
    """Validator and loader for flashcard JSON datasets."""

    @staticmethod
    def load_from_file(file_path: str) -> List[Dict[str, Any]]:
        """
        Loads flashcards from a JSON file, validating its schema.

        Args:
            file_path: Path to the JSON file.

        Returns:
            A list of dictionary objects representing validated flashcards.

        Raises:
            FileNotFoundError: If the file does not exist.
            FlashcardValidationError: If the JSON is invalid, missing
                                      required fields, or has an
                                      unsupported format.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise FlashcardValidationError(
                f"Invalid JSON syntax in {file_path}: {e}"
            )
        except IOError as e:
            raise FlashcardValidationError(
                f"Failed to read file {file_path}: {e}"
            )

        return FlashcardLoader.validate_and_parse(data)

    @staticmethod
    def validate_and_parse(data: Any) -> List[Dict[str, Any]]:
        """
        Validates and parses the JSON data into a uniform flashcard structure.

        Supports two input formats:
        1. Array Format: [{"front": "...", "back": "..."}]
        2. Object Format: {"cards": [{"front": "...", "back": "..."}]}

        Args:
            data: Loaded JSON content.

        Returns:
            A list of dictionary objects representing validated flashcards.

        Raises:
            FlashcardValidationError: If validation fails.
        """
        cards: List[Any] = []
        if isinstance(data, list):
            cards = data
        elif isinstance(data, dict):
            if "cards" not in data:
                raise FlashcardValidationError(
                    "Object format JSON must contain a 'cards' key."
                )
            cards = data["cards"]
            if not isinstance(cards, list):
                raise FlashcardValidationError("'cards' value must be a list.")
        else:
            raise FlashcardValidationError(
                "JSON root must be either a list or an object."
            )

        validated_cards: List[Dict[str, Any]] = []
        for idx, card in enumerate(cards):
            if not isinstance(card, dict):
                raise FlashcardValidationError(
                    f"Card at index {idx} is not a valid object."
                )
            if "front" not in card:
                raise FlashcardValidationError(
                    f"Card at index {idx} is missing "
                    "the required 'front' field."
                )
            if "back" not in card:
                raise FlashcardValidationError(
                    f"Card at index {idx} is missing "
                    "the required 'back' field."
                )

            front = card.get("front")
            back = card.get("back")

            if not isinstance(front, str) or not isinstance(back, str):
                raise FlashcardValidationError(
                    f"Card at index {idx} fields 'front' "
                    "and 'back' must be strings."
                )

            validated_cards.append(
                {"front": front.strip(), "back": back.strip()}
            )

        return validated_cards
