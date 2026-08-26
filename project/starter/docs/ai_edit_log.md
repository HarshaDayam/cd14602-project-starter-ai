# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

### 2024-01-15 - Initial Task Manager Implementation

**Context:** I needed to create a basic task management system to demonstrate CRUD operations and serve as the foundation for the project.

**AI Tool Used:** Claude

**Prompt/Request:** "Help me create a Python class for managing tasks with basic CRUD operations. The class should handle task creation, retrieval, completion, and deletion. Include proper error handling and type hints."

**AI Response:** Claude generated a TaskManager class with methods for add_task, get_task, get_all_tasks, complete_task, delete_task, and to_dict. The code included type hints, proper error handling with ValueError for missing tasks, and used datetime for timestamps.

**Changes Made:** 
- Added priority field to tasks with a default value of "medium"
- Modified the task structure to include created_at timestamp
- Added validation for priority values
- Renamed some variable names for clarity

**Reasoning:** 
- Priority field will be useful for implementing sorting features later
- Timestamps help with task organization and analytics
- Input validation prevents invalid data from being stored
- Better variable names improve code readability

**Outcome:** Successfully created a robust TaskManager class that serves as the core of the application with room for future enhancements.

**Lessons Learned:** 
- AI provides good starting implementations but always needs customization
- It's important to think about future requirements when reviewing AI code
- Type hints and error handling are crucial for maintainable code

---

## Your Log Entries

### 2026-08-26 - Flashcard Schema Validation Implementation

**Context:** I needed to build a validation utility that handles both array format `[{"front": "...", "back": "..."}]` and dictionary format `{"cards": [...]}` for incoming flashcard datasets.

**AI Tool Used:** Gemini 3.5 Flash

**Prompt/Request:** "Write a static validator class in Python that accepts a parsed JSON structure, verifies that it conforms to either list of dict format or dict with 'cards' key list of dict format, raises custom exception FlashcardValidationError for missing fields or bad types, and returns a uniform list of dicts."

**AI Response:** The AI generated a validator that implemented recursive type checking but did not handle empty objects or verify that fields were specifically strings.

**Changes Made:** 
- Added explicit type assertions to guarantee that `front` and `back` values are strings.
- Implemented `strip()` on strings during parsing to clean up loaded whitespace.
- Added comprehensive coverage tests for missing fields, bad types, and nonexistent files.

**Reasoning:** 
- Flashcards must contain text content; verifying string type explicitly prevents unexpected runtime errors in the CLI layer.
- Whitespace stripping makes answer matching more reliable.

**Outcome:** Clean validation logic that processes file errors and schema errors, providing helpful feedback to the console without raw tracebacks.

**Lessons Learned:** AI models sometimes overlook basic type consistency checks (like verifying string vs. int) unless explicitly prompted, making strict human verification essential.

---

### 2026-08-26 - Strategy Pattern for Quiz Modes

**Context:** I needed to implement the core quiz mechanics utilizing the Strategy Pattern to decouple the UI from specific questioning strategies (Sequential, Random, Adaptive).

**AI Tool Used:** Gemini 3.5 Flash

**Prompt/Request:** "Generate a Strategy pattern implementation for QuizMode abstract class with SequentialMode, RandomMode, and AdaptiveMode concrete strategies. For AdaptiveMode, when the user gets it wrong, the card should be re-queued so it repeats."

**AI Response:** The AI generated the inheritance structure correctly but initialized `self.current_card = None` inside the `AdaptiveMode` constructor and saved state redundantly.

**Changes Made:** 
- Removed `self.current_card` state variable completely.
- Refactored `next_card` to directly return `self.queue[0]`.
- Simplified the `record_result` check to directly inspect `self.queue[0]`.

**Reasoning:** 
- Eliminating unnecessary instance variables reduces object state complexity and resolves type-inference warnings in mypy.
- Returning elements directly from the queue makes the class stateless for active questions.

**Outcome:** A clean Strategy hierarchy that passes all mypy type checks and is fully testable.

**Lessons Learned:** Code generated by AI assistants often contains boilerplate instance variables that are never read; simplifying state is an important refactoring step.

---

### 2026-08-26 - Graceful KeyboardInterrupt and Exit Handling

**Context:** I needed to implement a robust CLI loop in `main.py` that intercepts Ctrl+C (KeyboardInterrupt) and exits cleanly when the user types 'exit'.

**AI Tool Used:** Gemini 3.5 Flash

**Prompt/Request:** "Create a main CLI loop that prompts the user with the front of a flashcard, reads input, matches answers case-insensitively, catches KeyboardInterrupt and 'exit' inputs, and prints current session statistics before calling sys.exit."

**AI Response:** The AI suggested catching KeyboardInterrupt inside the inner loop and using `sys.exit(0)`.

**Changes Made:** 
- Re-raised KeyboardInterrupt from the inner loop to the outer loop to ensure clean, centralized cleanup logic.
- Wrapped CLI statistics saving so that stats are only written if at least one question was attempted.

**Reasoning:** 
- Centralized exception handling makes the control flow cleaner and easier to follow.
- Writing statistics for 0 attempted questions clutters historical stats with empty entries.

**Outcome:** A robust terminal CLI that exits gracefully under all terminate conditions.

**Lessons Learned:** AI code suggestions often disperse cleanup routines across multiple nested try-except blocks; refactoring to a centralized exit point improves maintainability.

---

### 2026-08-26 - Mocking CLI Stdin/Stdout for Integration Testing

**Context:** I needed to write integration tests for the CLI session simulation using pytest.

**AI Tool Used:** Gemini 3.5 Flash

**Prompt/Request:** "How can I simulate a KeyboardInterrupt inside pytest when testing the main.main CLI execution without actually interrupting the test runner?"

**AI Response:** The AI recommended patching `builtins.input` with a `side_effect=KeyboardInterrupt`.

**Changes Made:** 
- Wrapped the `main.main()` invocation with a `pytest.raises(SystemExit)` context block.
- Added assertion `assert excinfo.value.code == 0` to verify a successful exit status.
- Patched the `FileHandler.__init__` path to redirect quiz stats to a temporary folder (`tmp_path`) to keep the workspace clean.

**Reasoning:** 
- Catching `SystemExit` is required when testing functions that call `sys.exit`.
- Redirecting stats file writing prevents test execution from modifying local history files.

**Outcome:** Highly thorough integration tests passing with 99% coverage on `tests/test_integration.py`.

**Lessons Learned:** Testing CLI applications with global side effects (like file writes and sys.exit) requires mocking and temporary environments.

---

### 2026-08-26 - Strict PEP 8 Line Length Compliance

**Context:** I needed to fix styling warnings from `flake8` about lines exceeding 79 characters.

**AI Tool Used:** Gemini 3.5 Flash

**Prompt/Request:** "Reformat these long docstrings and string comments to adhere to PEP 8 line length limits (maximum 79 characters)."

**AI Response:** The AI suggested wrapping strings with parenthesized continuation blocks.

**Changes Made:** 
- Wrapped all multi-line error strings and arguments into nested parenthesized implicit concatenations.
- Formatted comment blocks and class docstrings to strictly wrap at 79 chars.
- Ran `black --line-length 79` and `isort --line-length 79` to enforce spacing.

**Reasoning:** 
- Conforming strictly to PEP 8 ensures zero style violations and matches professional engineering guidelines.

**Outcome:** Codebase passes `flake8` checks with a 100% success rate.

**Lessons Learned:** Code formatters like Black may not wrap long string literals or comments automatically; manual line-wrapping is still necessary.

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
   - Generating architectural boilerplate (abstract base classes, Strategy class methods, and Factory selectors).
   - Designing base unit test cases and simulating user keyboard inputs and arguments using mocks.

2. **Where did you need to make the most modifications to AI suggestions?**
   - Resolving type constraints: Fixing implicit `None` initializations that triggered mypy type checking warnings.
   - PEP 8 formatting: Wrapping long strings and docstrings to keep lines strictly under 79 characters.

3. **What patterns did you notice in AI strengths and weaknesses?**
   - **Strengths**: Quick generation of design patterns, functional logic templates, and test scripts.
   - **Weaknesses**: Neglecting strict style formats (E501 line lengths) and introducing redundant variable states.

4. **How did your prompting technique improve over time?**
   - I transitioned from generic logic requests to specifying precise requirements up front, such as custom error rules, return types, and code constraints.

5. **What would you do differently in future AI collaborations?**
   - Configure formatting rules and static checkers (flake8, mypy) before prompting the AI, and include style limits directly within the prompt constraints.

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** 8
- **Lines of AI-generated code used:** ~400
- **Lines of AI-generated code modified:** ~120
- **Most helpful AI interaction:** Strategy Pattern draft for quiz strategies
- **Most challenging AI interaction:** Mypy type-check cleanup for None values
- **Biggest lesson learned:** Vetting variable side-effects and typing is key

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.