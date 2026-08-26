# AI-Assisted Development Project Report

**Student Name:** Rekha
**Project Title:** Flashcard Quizzer CLI Application
**Date:** August 26, 2026

## Executive Summary

The Flashcard Quizzer CLI Application is a Python-based utility designed to help students and developers study various topics through terminal-based quiz sessions. The application features multiple questioning strategies, handles custom JSON schemas for flashcard inputs, supports colored terminal feedback, and tracks quiz progress across study sessions. By utilizing design patterns like the Strategy and Factory patterns, the codebase maintains a clean separation of concerns and robust extensibility.

The development of the application was executed through a structured, iterative collaboration with the Antigravity AI coding assistant. The AI assistant was leveraged to construct core validation code, design the quiz mode strategy structures, and draft comprehensive unit tests. Over five major iterations, AI-suggested code was systematically reviewed, refined for type safety, and reformatted to comply with strict PEP 8 and mypy standards. 

This project demonstrates the effectiveness of AI collaboration when paired with strict human-in-the-loop software engineering practices. The result is a highly tested, well-structured command-line application that achieves over 90% code coverage while maintaining zero style violations.

---

## Project Overview

### Problem Statement
Self-directed study using digital flashcards is a widely accepted technique for learning new programming languages or concepts. However, existing command-line study tools are either too simple (lacking adaptive repetition) or overly complex with heavy dependencies. Furthermore, many tools are fragile, crashing when encountering malformed JSON schemas or invalid user files. There is a need for a lightweight, robust command-line flashcard application that supports multiple study modes (especially prioritized incorrect questions) and handles errors gracefully without raw tracebacks.

### Solution Approach
We built a CLI application using Python's standard library to keep dependencies light and load times minimal. 
Key design decisions include:
1. **Separation of Concerns**: We isolated file loading/validation (`utils/flashcard_loader.py`), persistence (`utils/file_handler.py`), strategy execution (`utils/quiz_engine.py`), and user interface orchestration (`main.py`).
2. **Strategy Pattern**: Abstracting the questioning algorithm allows us to plug in different behaviors at runtime.
3. **Factory Pattern**: Encapsulating object instantiation logic prevents UI code from depending directly on concrete strategy subclasses.
4. **ANSI Styling**: Providing clear, non-intrusive red/green color indicators for incorrect/correct answers.

### Final Features
- [x] Dual JSON schema validation support (Array Format and wrapper Object Format).
- [x] Three interactive quiz modes: Sequential, Random, and Adaptive.
- [x] Adaptive study logic that repeats incorrect questions until mastered.
- [x] Persistence of historical session statistics (number of quizzes, accuracy, correct/incorrect counters).
- [x] Graceful exit handling on both the "exit" command and KeyboardInterrupt (Ctrl+C).

---

## AI Collaboration Experience

### AI Tools Used
- **Antigravity (Gemini 3.5 Flash)**: Core pair-programming assistant used for code generation, test design, static typing validation, and formatting checks.

### Collaboration Workflow
1. **Planning & Prompting**: I started by describing the high-level architecture and constraints in a prompt.
2. **Review & Critical Analysis**: For every module the AI generated, I inspected the code to identify type-checking issues (like un-typed `Optional` values), redundant attributes (such as unused variables in `AdaptiveMode`), and PEP 8 line length violations.
3. **Iterative Refinement**: I directed the AI to refactor code blocks sequentially rather than rewriting entire files, minimizing tokens and ensuring precise edits.
4. **Validation**: I ran automated formatters (`black`, `isort`), linters (`flake8`), type checkers (`mypy`), and test frameworks (`pytest`) inside the virtual environment to ensure correctness.

### Most Valuable AI Interactions

#### Example 1: Schema Validation Rules
- **Context:** I needed a validation utility that could read two distinct formats of JSON datasets and raise custom validation errors rather than generic Python parsing errors.
- **AI Prompt:** "Write a static validator class in Python that accepts a parsed JSON structure, verifies that it conforms to either `[{"front": "str", "back": "str"}]` or `{"cards": [...]}` format, raises custom exception `FlashcardValidationError` for missing fields or bad types, and returns a uniform list of dicts."
- **AI Response:** The AI generated a clean validator using recursive type checks but overlooked empty list structures and non-string inputs.
- **Your Changes:** I added robust checks to ensure that the keys `front` and `back` are string types specifically and strip unnecessary whitespace from fields.
- **Outcome:** A robust data loader that catches bad files immediately and outputs user-friendly warnings.

#### Example 2: Strategy Pattern for Quiz Engine
- **Context:** Implementing the Sequential, Random, and Adaptive modes using the Strategy pattern.
- **AI Prompt:** "Generate a Strategy pattern implementation for `QuizMode` abstract class with SequentialMode, RandomMode, and AdaptiveMode concrete strategies. For AdaptiveMode, when the user gets it wrong, the card should be re-queued so it repeats."
- **AI Response:** The AI generated three classes inheriting from `QuizMode` and used an instance variable `self.current_card = None` to store the active question.
- **Your Changes:** During mypy type checking, the `self.current_card = None` assignment raised type mismatch warnings. I realized `self.current_card` was not accessed anywhere else in the code, so I refactored the classes to remove this state entirely and return the list elements directly.
- **Outcome:** Clean, warn-free, highly readable strategy implementations.

#### Example 3: Mocking CLI KeyboardInterrupt
- **Context:** Writing integration tests for KeyboardInterrupt (Ctrl+C) behavior inside the CLI main loop.
- **AI Prompt:** "How can I simulate a `KeyboardInterrupt` inside pytest when testing the `main.main` CLI execution without actually interrupting the test runner?"
- **AI Response:** The AI suggested using `unittest.mock.patch` on `builtins.input` with a `side_effect=KeyboardInterrupt`.
- **Your Changes:** When running the test, it initially failed because `main.main` called `sys.exit(0)` when catching the interrupt, which raised `SystemExit: 0` to the test runner. I added a `pytest.raises(SystemExit)` block to assert the correct exit code.
- **Outcome:** Full testing coverage of graceful abort routines.

### Challenges with AI Collaboration
- **Mypy Type Inference**: The AI frequently generated code using `None` initialization without `Optional` types, which triggers type errors under strict mypy configurations.
- **Strict Line Lengths**: The AI habitually produced comments and code lines longer than 79 characters, which failed strict PEP 8 checks. I resolved this by instructing `black` to format with `--line-length 79`.

---

## Software Engineering Practices

### Code Quality Measures
- **PEP 8 Compliance**: Enforced using `black` and `isort` with a strict limit of 79 characters, checked by `flake8`.
- **Static Typing**: All function signatures have type annotations validated by `mypy`.
- **Defensive Error Handling**: Catching and re-wrapping file/schema errors to show clean user messages.

### Testing Strategy
We wrote a comprehensive pytest suite located in `tests/`:
- `test_flashcard_loader.py`: Verifies formatting checks, invalid syntax, missing fields, and incorrect types.
- `test_quiz_modes.py`: Verifies factory strategy loading and correct adaptive queue behavior.
- `test_integration.py`: Simulates full CLI game sessions, early exits, missing arguments, and statistics outputs.
- **Result**: The project achieves a **92% code coverage** rating.

### Design Patterns Used
- **Strategy Pattern**: The abstract `QuizMode` acts as the strategy interface. `SequentialMode`, `RandomMode`, and `AdaptiveMode` implement distinct algorithms for serving questions.
- **Factory Pattern**: `QuizModeFactory` acts as a parameterized factory, returning the appropriate `QuizMode` instance based on the user's chosen CLI argument.

### Code Structure and Organization
```
starter/
├── main.py                 # CLI orchestration and color output
├── utils/
│   ├── file_handler.py     # Persistent statistics IO
│   ├── flashcard_loader.py # JSON schema loading and validation
│   └── quiz_engine.py      # Strategy and Factory quiz structures
└── tests/
    ├── test_flashcard_loader.py
    ├── test_integration.py
    └── test_quiz_modes.py
```

---

## Technical Challenges and Solutions

### Challenge 1: Adaptive Repeating Logic
- **Problem:** Making sure the user repeats incorrect cards until they answer them correctly, without creating infinite loops or throwing off stats.
- **Solution:** In `AdaptiveMode`, we pop the card from the front of the queue. If correct, it is removed; if incorrect, it is appended to the back of the queue. The session only terminates when the queue length is zero.
- **AI Involvement:** The AI proposed this queue structure which worked beautifully.

---

## Code Quality Analysis

### Metrics
- **Lines of code**: ~440 source lines, ~170 test lines.
- **Test coverage**: 92%
- **Number of functions/classes**: 7 classes, 5 helper/main functions.
- **Linting score**: 100% clean (0 errors reported by flake8/mypy).

### Self-Assessment
- **Code Readability (5/5)**: The code is cleanly modularized, contains descriptive docstrings for all modules, and strictly conforms to formatting standards.
- **Code Maintainability (5/5)**: Adding new quiz modes only requires creating a new strategy class in `quiz_engine.py` and adding it to the factory.
- **Test Quality (5/5)**: Standard and edge cases are validated, including mock IO integration tests.

---

## Learning Outcomes

### Technical Skills Developed
- Standard Strategy and Factory patterns in Python.
- Advanced unit testing using `pytest` with mock side effects and capture fixtures.
- Custom validation logic for multiple JSON schemas.

### AI Collaboration Skills
- Writing targeted prompts to receive refactored snippets instead of massive rewrites.
- Critically reviewing AI code for PEP 8 compliance and static typing before integration.

---

## Reflection

### What Worked Well
Using `black` with strict line length checks was very helpful in resolving PEP 8 issues quickly. Mocking `sys.argv` and `builtins.input` allowed us to test the entire CLI programmatically.

### Future Enhancements
- Adding support for importing CSV/TSV flashcards.
- Adding timed quizzes to challenge the user.

---

## Conclusion
Pair programming with AI coding assistants is a highly productive workflow when coupled with rigorous engineering standards. By treating the AI assistant as a junior developer whose output must be vetted and formatted, we constructed a reliable, clean, and fully tested Flashcard Quizzer application.
