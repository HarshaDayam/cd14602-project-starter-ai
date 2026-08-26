"""
Integration tests for the Flashcard Quizzer CLI Application.
"""

from unittest.mock import patch

import pytest

import main
from utils.file_handler import FileHandler


def test_full_session(tmp_path, capsys):
    """Simulates a full CLI session with 3 questions,
    verifying stats calculation."""
    # 1. Create a temporary flashcard file
    file = tmp_path / "integration_cards.json"
    file.write_text(
        '[{"front": "Q1", "back": "A1"}, '
        '{"front": "Q2", "back": "A2"}, '
        '{"front": "Q3", "back": "A3"}]',
        encoding="utf-8",
    )

    # 2. Simulate inputs: User answers Q1 correctly ("A1"),
    # Q2 incorrectly ("Wrong"), Q3 correctly ("A3")
    inputs = ["A1", "Wrong", "A3"]

    # Clear cumulative stats file first so we test fresh saving behavior
    stats_file = tmp_path / "quiz_stats.json"
    if stats_file.exists():
        stats_file.unlink()

    # Patch FileHandler.__init__ to use tmp_path as the data directory
    with patch.object(
        FileHandler,
        "__init__",
        lambda self, data_dir=str(tmp_path): setattr(
            self, "data_dir", tmp_path
        ),
    ):
        with patch("builtins.input", side_effect=inputs):
            with patch(
                "sys.argv", ["main.py", "-f", str(file), "-m", "sequential"]
            ):
                main.main()

    # 3. Capture and verify stdout
    captured = capsys.readouterr()
    output = captured.out

    # Check that questions were printed
    assert "Question:" in output
    assert "Q1" in output
    assert "Q2" in output
    assert "Q3" in output

    # Check color/text feedback was shown
    assert "Correct!" in output
    assert "Incorrect!" in output

    # Check session summary values
    assert "Session Summary" in output
    assert "Questions Attempted: 3" in output
    assert "Correct Answers:     " in output  # With color code prefix
    assert "Incorrect Answers:   " in output
    assert "Session Accuracy:    66.7%" in output


def test_cli_graceful_exit_early(tmp_path, capsys):
    """Verifies typing 'exit' terminates the session gracefully with
    summary stats."""
    file = tmp_path / "integration_cards.json"
    file.write_text(
        '[{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]',
        encoding="utf-8",
    )

    inputs = ["exit"]

    with patch.object(
        FileHandler,
        "__init__",
        lambda self, data_dir=str(tmp_path): setattr(
            self, "data_dir", tmp_path
        ),
    ):
        with patch("builtins.input", side_effect=inputs):
            with patch(
                "sys.argv", ["main.py", "-f", str(file), "-m", "sequential"]
            ):
                main.main()

    captured = capsys.readouterr()
    output = captured.out

    assert "Quiz exited early." in output
    assert "Questions Attempted: 0" in output


def test_cli_keyboard_interrupt(tmp_path, capsys):
    """Verifies that Ctrl+C (KeyboardInterrupt) exits gracefully with
    summary stats."""
    file = tmp_path / "integration_cards.json"
    file.write_text('[{"front": "Q1", "back": "A1"}]', encoding="utf-8")

    with patch.object(
        FileHandler,
        "__init__",
        lambda self, data_dir=str(tmp_path): setattr(
            self, "data_dir", tmp_path
        ),
    ):
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            with patch("sys.argv", ["main.py", "-f", str(file)]):
                with pytest.raises(SystemExit) as excinfo:
                    main.main()
                assert excinfo.value.code == 0

    captured = capsys.readouterr()
    output = captured.out

    assert "Quiz interrupted by user. Exiting..." in output
    assert "Questions Attempted: 0" in output


def test_cli_missing_arguments(capsys):
    """Verifies CLI prints error message and exits when no arguments
    are provided."""
    with patch("sys.argv", ["main.py"]):
        with pytest.raises(SystemExit) as excinfo:
            main.main()
    assert excinfo.value.code == 1

    captured = capsys.readouterr()
    assert "Error: Please specify a flashcard file" in captured.out


def test_cli_stats_display_only(tmp_path, capsys):
    """Verifies CLI displays statistics and exits when --stats is
    requested without a file."""
    # Write some stats first
    fh = FileHandler(str(tmp_path))
    stats = {
        "quizzes_played": 2,
        "total_questions": 10,
        "total_correct": 8,
        "total_incorrect": 2,
    }
    fh.save_data("quiz_stats.json", stats)

    with patch.object(
        FileHandler,
        "__init__",
        lambda self, data_dir=str(tmp_path): setattr(
            self, "data_dir", tmp_path
        ),
    ):
        with patch("sys.argv", ["main.py", "--stats"]):
            with pytest.raises(SystemExit) as excinfo:
                main.main()
            assert excinfo.value.code == 0

    captured = capsys.readouterr()
    output = captured.out
    assert "Quiz Statistics History" in output
    assert "Quizzes Played:    2" in output
    assert "Overall Accuracy:  80.0%" in output
