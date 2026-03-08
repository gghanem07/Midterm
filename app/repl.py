from decimal import Decimal

from colorama import Fore, Style, init

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory

init(autoreset=True)


def calculator_repl():
    calc = Calculator()

    calc.add_observer(LoggingObserver())
    calc.add_observer(AutoSaveObserver(calc))

    print(Fore.CYAN + "midterm-calc started. Type 'help' for commands.")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "help":
            print(Fore.YELLOW + "\nCommands:")
            print(" add subtract multiply divide power root modulus intdiv percentage absdiff")
            print(" history clear undo redo save load")
            print(" exit")
            continue

        if command == "exit":
            calc.save_history()
            print(Fore.CYAN + "Goodbye")
            break

        if command == "history":
            history = calc.show_history()
            if not history:
                print(Fore.YELLOW + "No history")
            else:
                print(Fore.YELLOW + "Calculation History:")
                for i, entry in enumerate(history, 1):
                    print(f"{i}. {entry}")
            continue

        if command == "clear":
            calc.clear_history()
            print(Fore.YELLOW + "History cleared")
            continue

        if command == "undo":
            print(Fore.YELLOW + ("Undone" if calc.undo() else "Nothing to undo"))
            continue

        if command == "redo":
            print(Fore.YELLOW + ("Redone" if calc.redo() else "Nothing to redo"))
            continue

        if command == "save":
            calc.save_history()
            print(Fore.YELLOW + "History saved")
            continue

        if command == "load":
            calc.load_history()
            print(Fore.YELLOW + "History loaded")
            continue

        try:
            op = OperationFactory.create_operation(command)
        except ValueError:
            print(Fore.RED + "Unknown command. Type 'help' to see available commands.")
            continue

        try:
            a = input("First number: ")
            b = input("Second number: ")

            calc.set_operation(op)
            result = calc.perform_operation(a, b)

            if isinstance(result, Decimal):
                result = format(result, "f")

            print(Fore.GREEN + f"Result: {result}")

        except (ValidationError, OperationError) as e:
            print(Fore.RED + f"Error: {e}")
        except Exception as e:
            print(Fore.RED + f"Unexpected error: {e}")


if __name__ == "__main__":
    calculator_repl()