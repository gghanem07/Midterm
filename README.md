Midterm - Calculator Command-Line Application

Overview

The project is a Python-based command-line calculator application, the application
supports multiple mathematical operations, persistent history storage,
undo/redo functionality, environment-based configuration, logging, and
automated testing with high coverage.


Features

Core Calculator Operations - Addition - Subtraction - Multiplication -
Division - Power - Root - Modulus - Integer Division - Percentage -
Absolute Difference

History Management - Persistent history stored as CSV - History
viewing - Clear history - Undo / redo operations

Configuration - Environment variables using .env - Configurable history
size - Configurable decimal precision - Configurable log and history
directories

Logging - Logging of calculator events - Stored in logs/calculator.log

Data Handling - Uses pandas to store and manage calculation history -
History saved to CSV automatically

Observers - Auto-save observer - Logging observer

Command Line Interface - Interactive REPL (Read–Eval–Print Loop) -
Color-coded output using Colorama

Testing - Unit tests implemented with pytest - Coverage tracking with
pytest-cov - Project coverage target ≥ 90%

Project Structure

app/ calculation.py calculator.py calculator_config.py
calculator_memento.py exceptions.py history.py input_validators.py
logger.py operations.py repl.py

tests/ test_calculation.py test_calculation_more.py test_calculator.py
test_config.py test_history.py test_operations.py test_repl.py
test_repl_more.py test_validators.py

data/ logs/

requirements.txt README.md .env

Installation

1.  Clone the repository

    git clone https://github.com/your-repository/Midterm.git 
	cd Midterm

2.  Create a virtual environment

    python -m venv venv

3.  Activate the environment

 source venv/bin/activate

Windows: venv

4.  Install dependencies

    pip install -r requirements.txt

Running the Calculator

Start the command-line calculator:

    python -m app.repl

Available Commands

Math operations: - add - subtract - multiply - divide - power - root -
modulus - intdiv - percentage - absdiff

History commands: - history - clear - undo - redo - save - load

System commands: - help - exit

Environment Configuration (.env)

Example .env file:

CALCULATOR_MAX_HISTORY_SIZE=100 CALCULATOR_PRECISION=10
CALCULATOR_LOG_DIR=logs CALCULATOR_HISTORY_DIR=data/history
CALCULATOR_AUTO_SAVE=true

Running Tests

Run all tests:

    pytest

Run tests with coverage:

    pytest --cov=app --cov-report=term-missing


CI/CD information:

GitHub Actions automatically runs tests and coverage checks on each push
to ensure the project remains stable and meets quality requirements.

tools Used

-   Python
-   pandas
-   numpy
-   pytest
-   pytest-cov
-   python-dotenv
-   colorama
