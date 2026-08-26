"""
Main entry point for the Flashcard Quizzer CLI Application.
"""

import argparse
import sys
from typing import Dict

from utils.file_handler import FileHandler
from utils.flashcard_loader import FlashcardLoader, FlashcardValidationError
from utils.quiz_engine import QuizModeFactory

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
YELLOW = "\033[93m"


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(
        description="Flashcard Quizzer CLI Application"
    )
    parser.add_argument(
        "-f", "--file", help="Path to the flashcard JSON file."
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["sequential", "random", "adaptive"],
        default="sequential",
        help="Quiz mode strategy to use (default: sequential).",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display historical quiz statistics and exit.",
    )
    return parser.parse_args()


def show_stats(file_handler: FileHandler) -> None:
    """Displays cumulative historical quiz statistics."""
    stats = file_handler.load_data("quiz_stats.json")
    if not stats:
        print("\nNo quiz statistics found. Play a game first!\n")
        return

    quizzes = stats.get("quizzes_played", 0)
    total = stats.get("total_questions", 0)
    correct = stats.get("total_correct", 0)
    incorrect = stats.get("total_incorrect", 0)
    accuracy = (correct / total * 100) if total > 0 else 0.0

    print("\n" + "=" * 40)
    print(f"{BOLD}Quiz Statistics History{RESET}")
    print("=" * 40)
    print(f"Quizzes Played:    {quizzes}")
    print(f"Total Questions:   {total}")
    print(f"Correct Answers:   {GREEN}{correct}{RESET}")
    print(f"Incorrect Answers: {RED}{incorrect}{RESET}")
    print(f"Overall Accuracy:  {accuracy:.1f}%")
    print("=" * 40 + "\n")


def save_session_stats(
    file_handler: FileHandler, correct: int, incorrect: int
) -> None:
    """Saves session statistics to the cumulative history."""
    stats = file_handler.load_data("quiz_stats.json")
    stats["quizzes_played"] = stats.get("quizzes_played", 0) + 1
    stats["total_questions"] = (
        stats.get("total_questions", 0) + correct + incorrect
    )
    stats["total_correct"] = stats.get("total_correct", 0) + correct
    stats["total_incorrect"] = stats.get("total_incorrect", 0) + incorrect
    file_handler.save_data("quiz_stats.json", stats)


def print_session_summary(stats: Dict[str, int]) -> None:
    """Prints a summary of the current quiz session."""
    correct = stats.get("correct", 0)
    incorrect = stats.get("incorrect", 0)
    total = correct + incorrect
    accuracy = (correct / total * 100) if total > 0 else 0.0

    print("\n" + "=" * 40)
    print(f"{BOLD}Session Summary{RESET}")
    print("=" * 40)
    print(f"Questions Attempted: {total}")
    print(f"Correct Answers:     {GREEN}{correct}{RESET}")
    print(f"Incorrect Answers:   {RED}{incorrect}{RESET}")
    print(f"Session Accuracy:    {accuracy:.1f}%")
    print("=" * 40 + "\n")


def main() -> None:
    """Main execution path for the CLI application."""
    args = parse_arguments()
    file_handler = FileHandler()

    if args.stats:
        show_stats(file_handler)
        if not args.file:
            sys.exit(0)

    if not args.file:
        print(
            f"{RED}Error: Please specify a flashcard file with -f/--file, "
            f"or view stats with --stats.{RESET}"
        )
        sys.exit(1)

    try:
        cards = FlashcardLoader.load_from_file(args.file)
    except FileNotFoundError:
        print(f"{RED}Error: Flashcard file '{args.file}' not found.{RESET}")
        sys.exit(1)
    except FlashcardValidationError as e:
        print(f"{RED}Error loading flashcards: {e}{RESET}")
        sys.exit(1)

    try:
        quiz = QuizModeFactory.get_mode(args.mode, cards)
    except ValueError as e:
        print(f"{RED}Error: {e}{RESET}")
        sys.exit(1)

    print(f"\n{BLUE}Starting Flashcard Quizzer!{RESET}")
    print(f"Mode: {BOLD}{args.mode.capitalize()}{RESET}")
    print(
        f"Loaded {len(cards)} flashcards. Type 'exit' at any prompt to quit.\n"
    )

    try:
        while quiz.has_next():
            card = quiz.next_card()
            print(f"{BOLD}Question:{RESET} {card['front']}")
            try:
                user_answer = input(f"{BOLD}Your Answer:{RESET} ").strip()
            except KeyboardInterrupt:
                # Propagate to outer block to handle gracefully
                raise KeyboardInterrupt

            if user_answer.lower() == "exit":
                print(f"\n{YELLOW}Quiz exited early.{RESET}")
                break

            correct_ans = card["back"].strip()
            if user_answer.lower() == correct_ans.lower():
                print(f"{GREEN}Correct!{RESET}\n")
                quiz.record_result(card, True)
            else:
                print(
                    f"{RED}Incorrect!{RESET} The correct answer is: "
                    f"{GREEN}{correct_ans}{RESET}\n"
                )
                quiz.record_result(card, False)

        # After natural completion or 'exit' typed
        print_session_summary(quiz.stats)
        if quiz.stats["correct"] > 0 or quiz.stats["incorrect"] > 0:
            save_session_stats(
                file_handler, quiz.stats["correct"], quiz.stats["incorrect"]
            )

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Quiz interrupted by user. Exiting...{RESET}")
        print_session_summary(quiz.stats)
        if quiz.stats["correct"] > 0 or quiz.stats["incorrect"] > 0:
            save_session_stats(
                file_handler, quiz.stats["correct"], quiz.stats["incorrect"]
            )
        sys.exit(0)


if __name__ == "__main__":
    main()
