"""
Unit tests for the QuizMode subclasses and selection factory.
"""

import pytest

from utils.quiz_engine import (AdaptiveMode, QuizModeFactory, RandomMode,
                               SequentialMode)


def test_quiz_mode_factory():
    """Verifies that QuizModeFactory instantiates correct strategy objects."""
    cards = [{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]

    seq = QuizModeFactory.get_mode("sequential", cards)
    assert isinstance(seq, SequentialMode)

    rnd = QuizModeFactory.get_mode("random", cards)
    assert isinstance(rnd, RandomMode)

    adapt = QuizModeFactory.get_mode("adaptive", cards)
    assert isinstance(adapt, AdaptiveMode)

    # Empty cards case
    with pytest.raises(ValueError) as excinfo:
        QuizModeFactory.get_mode("sequential", [])
    assert "cannot be empty" in str(excinfo.value)

    # Invalid mode case
    with pytest.raises(ValueError) as excinfo:
        QuizModeFactory.get_mode("unsupported_mode", cards)
    assert "Unknown quiz mode" in str(excinfo.value)


def test_adaptive_mode_behavior():
    """Verifies that incorrect questions are appended back to the
    adaptive queue."""
    cards = [{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]
    mode = QuizModeFactory.get_mode("adaptive", cards)
    assert isinstance(mode, AdaptiveMode)

    # First question: Q1
    assert mode.has_next()
    c1 = mode.next_card()
    assert c1["front"] == "Q1"
    # User gets Q1 incorrect
    mode.record_result(c1, correct=False)

    # Second question: Q2 (because Q1 is pushed to the back)
    assert mode.has_next()
    c2 = mode.next_card()
    assert c2["front"] == "Q2"
    # User gets Q2 correct
    mode.record_result(c2, correct=True)

    # Third question: Q1 (repeated because it was incorrect earlier)
    assert mode.has_next()
    c3 = mode.next_card()
    assert c3["front"] == "Q1"
    # User gets Q1 correct this time
    mode.record_result(c3, correct=True)

    # Should have no more cards
    assert not mode.has_next()
    assert mode.stats["correct"] == 2
    assert mode.stats["incorrect"] == 1


def test_sequential_mode_behavior():
    """Verifies sequential presentation of flashcards."""
    cards = [{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]
    mode = QuizModeFactory.get_mode("sequential", cards)

    # First card
    assert mode.has_next()
    c1 = mode.next_card()
    assert c1["front"] == "Q1"
    mode.record_result(c1, correct=True)

    # Second card
    assert mode.has_next()
    c2 = mode.next_card()
    assert c2["front"] == "Q2"
    mode.record_result(c2, correct=False)

    # No more cards
    assert not mode.has_next()
    with pytest.raises(IndexError):
        mode.next_card()


def test_random_mode_behavior():
    """Verifies that all cards are presented exactly once in random mode."""
    cards = [
        {"front": "Q1", "back": "A1"},
        {"front": "Q2", "back": "A2"},
        {"front": "Q3", "back": "A3"},
    ]
    mode = QuizModeFactory.get_mode("random", cards)

    presented_fronts = []
    while mode.has_next():
        c = mode.next_card()
        presented_fronts.append(c["front"])
        mode.record_result(c, correct=True)

    assert len(presented_fronts) == 3
    assert set(presented_fronts) == {"Q1", "Q2", "Q3"}
