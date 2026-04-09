# CLI Layer

# Libraries
from colorama import init, Fore
from pathlib import Path
import argparse
import sys

# Project modules
from engine import ContactManager
from entity import validate_email, validate_name, validate_phone

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

# Check validations
def validate(arg, method):
    is_valid, error_msg = method(arg)
    if not is_valid:
        print_error(f"Command failed: {error_msg}")
        sys.exit(0)
    


# COMMANDS

# add command
def cmd_add(args):

    if not args:
        print("No arguments passed")
        sys.exit(0)

    try:
        # Validating inputs
        validate(args.name, validate_name)
        validate(args.phone, validate_phone)
        if args.email:
            validate(args.email, validate_email)
        
        result = cm.add_contact(name=args.name, phone=args.phone, email=args.email)
        if result:
            print_success(f"Contact '{args.name}' successfully added")
            sys.exit(0)
        else:
            print_error(f"Command failed")
            sys.exit(1)
    except Exception as e:
        print_error(e)
        print_error(f"Command failed")
        sys.exit(1)

# list command
def cmd_list():

    contacts = cm.list_all()

    if not contacts:
        print("No contacts found")
        sys.exit(0)

    headers = ["#", "Name", "Phone", "Email"]
    formatted_data = [
        [c[0], c[2], c[3], c[4] if c[4] else "-"]
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

    # Add parser
    add_parser = sub.add_parser("add", help="Add contact")
    add_parser.add_argument("--name", required= True)
    add_parser.add_argument("--phone", required=True)
    add_parser.add_argument("--email")

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
        
        elif args.command == "add":
            return cmd_add(args)

        else:
            print("Available commands: list")

    except KeyboardInterrupt:
        print_error(f"User cancelled")
        sys.exit(130)
        
    except Exception as e:
        print_error(e)
        sys.exit(1)

if __name__ == "__main__":
    run()