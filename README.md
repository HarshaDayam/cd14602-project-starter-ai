# Flashcard Quizzer CLI Application

Welcome to the **Flashcard Quizzer CLI Application**! This is a robust, lightweight command-line tool designed for studying flashcards using various quiz strategies. It supports customized study sessions, historical stats tracking, and an adaptive mode that repeats incorrect cards until they are mastered.

---

## 🚀 Features

1. **Robust Schema Validation**: Supports loading JSON files in two formats:
   - **Array Format**: A list of card objects: `[{"front": "...", "back": "..."}]`
   - **Object Format**: A wrapper object: `{"cards": [{"front": "...", "back": "..."}]}`
2. **Three Strategy Quiz Modes**:
   - **Sequential Mode**: Presents flashcards in their natural loaded order.
   - **Random Mode**: Shuffles cards randomly for unpredictable review sessions.
   - **Adaptive Mode**: Prioritizes cards you get incorrect, repeating them until they are answered correctly.
3. **Colored Terminal Feedback**: Uses ANSI colors (green for correct, red for incorrect) to make learning visually engaging.
4. **Historical Statistics**: Saves cumulative study stats (played count, total questions, correct/incorrect counters, accuracy) across sessions in `data/quiz_stats.json`.
5. **Graceful Terminate Routines**: Handles graceful exits on both the `"exit"` keyboard input and `Ctrl+C` interrupt, displaying session summaries before closing.

---

## 🛠️ Installation and Setup

1. **Navigate to the project root:**
   ```bash
   cd project/starter
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🎮 How to Play

### Run a Quiz Session
To run a quiz, specify the JSON flashcards file and your desired mode:
```bash
python main.py -f data/python_basics.json -m sequential
python main.py -f data/python_basics.json -m random
python main.py -f data/python_basics.json -m adaptive
```
*Tip: You can type `exit` at any prompt, or press `Ctrl+C` to quit early and view your session summary.*

### View Statistics
To view your cumulative history across all quiz runs:
```bash
python main.py --stats
```

---

## 🧪 Testing

The codebase includes a comprehensive test suite covering all validation rules, quiz patterns, and CLI integrations.

Run all tests and generate a coverage report:
```bash
pytest --cov=. --cov-report=term-missing
```

We aim for >80% code coverage. The current codebase achieves **92% coverage**.

---

## 🧹 Code Quality

We enforce strict coding guidelines. Verify code formatting and linting using:

```bash
# Code Formatting (Black)
black --check --line-length 79 .

# Import Organization (isort)
isort --check --profile black --line-length 79 .

# Linting (flake8)
flake8 --exclude=venv .

# Static Type Verification (mypy)
mypy --exclude venv .
```

---

## 📁 Project Structure

```
starter/
├── main.py                 # Main entry point (argparse, interactive CLI loop)
├── requirements.txt        # Project dependencies
├── data/
│   └── python_basics.json  # Sample basic Python study deck
├── utils/
│   ├── __init__.py
│   ├── file_handler.py     # IO loader for cumulative stats
│   ├── flashcard_loader.py # Schema validator
│   └── quiz_engine.py      # Abstract QuizMode strategy and factory structures
└── tests/
    ├── __init__.py
    ├── test_flashcard_loader.py  # Validator tests
    ├── test_quiz_modes.py        # Factory and Strategy behavior tests
    └── test_integration.py       # Full CLI integration tests
```

---

## 🎨 Design Patterns Implemented

- **Strategy Pattern**: Abstract base class `QuizMode` acts as the strategy interface, and `SequentialMode`, `RandomMode`, and `AdaptiveMode` implement the concrete questioning algorithms.
- **Factory Pattern**: `QuizModeFactory` acts as a parameterized factory class to instantiate and return the desired `QuizMode` subclass at runtime based on user configuration.
