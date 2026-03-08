# Enhanced Calculator Command-Line Application

## Project Description
This project is an enhanced calculator built as a command-line application using the REPL pattern (Read-Eval-Print Loop). It supports standard arithmetic operations as well as advanced operations such as power, root, modulus, integer division, percentage, and absolute difference.

The application also includes:
- Factory Design Pattern for creating operations
- Memento Design Pattern for undo/redo
- Observer Design Pattern for logging and auto-save
- CSV history persistence using pandas
- Configuration management with `.env`
- Automated testing with pytest and pytest-cov
- GitHub Actions CI workflow

## Features
Supported commands:
- `add`
- `subtract`
- `multiply`
- `divide`
- `power`
- `root`
- `modulus`
- `intdiv`
- `percentage`
- `absdiff`
- `history`
- `clear`
- `undo`
- `redo`
- `save`
- `load`
- `help`
- `exit`

## Installation Instructions

### 1. Clone the repository
```bash
git clone https://github.com/gghanem07/Midterm.git
cd Midterm

## 2. create and activate a virtual environment: 

python3 -m venv venv
source venv/bin/activate

## 3. install dependencies

pip install -r requirements.txt

## 4.configuration setup: 
create .env file in the project root: 

CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_PRECISION=10
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=data/history
CALCULATOR_AUTO_SAVE=true

## 5. Usage guide: 
to run the calculator use: 

python -m app.repl
python main.py

## 6. History and Persistence
view calculator history: history
clear calculator history: clear
Undo and redo are supported with: undo and undo 
History can be saved to CSV: save 
History can be loaded from CSV: load



## 7. Testing:
 run all tests:
pytest

run with rest coverage:
pytest --cov=app --cov-report=term-missing


## 8. CI/CD pipeline:
GitHub Actions is configured to automatically: 
- install dependencies 
- run tests 
- check code coverage 
the workflow file is located at: 

.github/workflows/python-app.yml

## 9. project structure: 

Midterm/
├── app/
│   ├── __init__.py
│   ├── calculator.py
│   ├── calculation.py
│   ├── calculator_config.py
│   ├── calculator_memento.py
│   ├── exceptions.py
│   ├── history.py
│   ├── input_validators.py
│   ├── logger.py
│   ├── operations.py
│   └── repl.py
├── tests/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
└── .github/workflows/python-app.yml
