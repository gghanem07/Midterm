from decimal import Decimal

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory


def calculator_repl():
    calc = Calculator()

    calc.add_observer(LoggingObserver())
    calc.add_observer(AutoSaveObserver(calc))

    print("midterm-calc started. Type 'help' for commands.")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "help":
            print("\nCommands:")
            print(" add subtract multiply divide power root")
            print(" history clear undo redo save load")
            print(" exit")
            continue

        if command == "exit":
            calc.save_history()
            print("Goodbye")
            break

        if command == "history":
            history = calc.show_history()
            if not history:
                print("No history")
            else:
                for i, entry in enumerate(history, 1):
                    print(f"{i}. {entry}")
            continue

        if command == "clear":
            calc.clear_history()
            print("History cleared")
            continue

        if command == "undo":
            print("Undone" if calc.undo() else "Nothing to undo")
            continue

        if command == "redo":
            print("Redone" if calc.redo() else "Nothing to redo")
            continue

        if command == "save":
            calc.save_history()
            print("History saved")
            continue

        if command == "load":
            calc.load_history()
            print("History loaded")
            continue

        try:
            op = OperationFactory.create_operation(command)

            a = input("First number: ")
            b = input("Second number: ")

            calc.set_operation(op)

            result = calc.perform_operation(a, b)

            if isinstance(result, Decimal):
                result = result.normalize()

            print("Result:", result)

        except (ValidationError, OperationError) as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)


if __name__ == "__main__":
    calculator_repl()