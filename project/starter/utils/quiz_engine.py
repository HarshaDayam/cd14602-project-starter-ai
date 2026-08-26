"""
Core quiz engine containing standard Strategy and Factory design patterns.
"""

import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class QuizMode(ABC):
    """Abstract base class for all quiz modes (Strategy Pattern)."""

    def __init__(self, cards: List[Dict[str, Any]]) -> None:
        """
        Initializes the quiz mode.

        Args:
            cards: A list of flashcards. Each card is a dictionary.
        """
        self.cards = cards
        self.stats = {"correct": 0, "incorrect": 0}

    @abstractmethod
    def has_next(self) -> bool:
        """Checks if there are more cards left in the quiz."""
        pass

    @abstractmethod
    def next_card(self) -> Dict[str, Any]:
        """Retrieves the next card in the quiz."""
        pass

    @abstractmethod
    def record_result(self, card: Dict[str, Any], correct: bool) -> None:
        """
        Records the answer result for the given card.

        Args:
            card: The card being answered.
            correct: True if user's answer was correct, False otherwise.
        """
        pass


class SequentialMode(QuizMode):
    """Sequential quiz mode: presents cards in the order they were loaded."""

    def __init__(self, cards: List[Dict[str, Any]]) -> None:
        super().__init__(cards)
        self.queue = list(cards)
        self.current_index = 0

    def has_next(self) -> bool:
        return self.current_index < len(self.queue)

    def next_card(self) -> Dict[str, Any]:
        if not self.has_next():
            raise IndexError("No more cards in sequential quiz mode.")
        card = self.queue[self.current_index]
        self.current_index += 1
        return card

    def record_result(self, card: Dict[str, Any], correct: bool) -> None:
        if correct:
            self.stats["correct"] += 1
        else:
            self.stats["incorrect"] += 1


class RandomMode(QuizMode):
    """Random quiz mode: presents cards in a randomly shuffled order."""

    def __init__(self, cards: List[Dict[str, Any]]) -> None:
        super().__init__(cards)
        self.queue = list(cards)
        random.shuffle(self.queue)
        self.current_index = 0

    def has_next(self) -> bool:
        return self.current_index < len(self.queue)

    def next_card(self) -> Dict[str, Any]:
        if not self.has_next():
            raise IndexError("No more cards in random quiz mode.")
        card = self.queue[self.current_index]
        self.current_index += 1
        return card

    def record_result(self, card: Dict[str, Any], correct: bool) -> None:
        if correct:
            self.stats["correct"] += 1
        else:
            self.stats["incorrect"] += 1


class AdaptiveMode(QuizMode):
    """
    Adaptive quiz mode: prioritizes cards the user gets wrong.
    Incorrect cards are appended to the end of the queue to be repeated.
    """

    def __init__(self, cards: List[Dict[str, Any]]) -> None:
        super().__init__(cards)
        self.queue = list(cards)

    def has_next(self) -> bool:
        return len(self.queue) > 0

    def next_card(self) -> Dict[str, Any]:
        if not self.has_next():
            raise IndexError("No more cards in adaptive quiz mode.")
        return self.queue[0]

    def record_result(self, card: Dict[str, Any], correct: bool) -> None:
        # Verify the recorded card is the one currently at the head
        # of the queue
        if self.queue and self.queue[0] == card:
            self.queue.pop(0)

        if not correct:
            self.queue.append(card)
            self.stats["incorrect"] += 1
        else:
            self.stats["correct"] += 1


class QuizModeFactory:
    """Factory Pattern to select the correct QuizMode subclass."""

    @staticmethod
    def get_mode(mode_name: str, cards: List[Dict[str, Any]]) -> QuizMode:
        """
        Creates a QuizMode instance based on the mode name.

        Args:
            mode_name: The string identifying the mode
                       (sequential, random, adaptive).
            cards: The list of flashcards to quiz.

        Returns:
            An instance of QuizMode.

        Raises:
            ValueError: If the mode name is unknown.
        """
        if not cards:
            raise ValueError("Flashcard list cannot be empty.")

        mode_lower = mode_name.lower()
        if mode_lower == "sequential":
            return SequentialMode(cards)
        elif mode_lower == "random":
            return RandomMode(cards)
        elif mode_lower == "adaptive":
            return AdaptiveMode(cards)
        else:
            raise ValueError(f"Unknown quiz mode: {mode_name}")
