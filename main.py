# CLI Layer

# Libraries
from colorama import init, Fore
from pathlib import Path
import argparse
import sys

# Project modules
from engine import ContactManager

# Directories and files
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CONTACT_FILE_PATH = DATA_DIR / "contacts.json"

# Initialize Contact Manager
cm = ContactManager(CONTACT_FILE=CONTACT_FILE_PATH)

# UI UTILITES

init(autoreset=True)
# Print error
def print_error(msg):
    print(Fore.RED + f"{msg}")

# Print success
def print_success(msg):
    print(Fore.GREEN + f"{msg}")


# COMMANDS

# list command
def cmd_list():

    contacts = cm.list_all()

    if not contacts:
        print("No contacts found")
        sys.exit(0)

    headers = ["#", "Name", "Phone", "Email"]
    formatted_data = [
        [c[0], c[2], c[3], c[4]]
        for c in contacts
    ]

    # Import tabulate
    from tabulate import tabulate
    print(tabulate(tabular_data=formatted_data, headers=headers))
    print()
    print_success(f"Total {len(contacts)} contact(s) fetched\n")
    sys.exit(0)

# help command
def cmd_help():

    print("CONTACT MANAGER".center(50, "-"))
    help_text = """
Welcome to Contact Manager CLI
"""

    print(help_text)
    sys.exit(0)


# Run commands
def run():

    # Argument parser
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    # List parser
    list_parser = sub.add_parser("list",help="List all contacts")

    # Help parser
    help_parser = sub.add_parser("help", help="Show usage and related information")
    

    # Execute
    try:
        args = parser.parse_args()
        if args.command == "list":
            return cmd_list()
        
        elif args.command == "help":
            return cmd_help()

        else:
            print("Available commands: list")
        
    except Exception as e:
        print_error(e)

if __name__ == "__main__":
    run()