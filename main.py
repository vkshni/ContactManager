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

# Print table
def print_table(data: list[list], headers: list):
    from tabulate import tabulate
    print(tabulate(data, headers=headers))
    


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

# search command
def cmd_search(args):

    if not args:
        print("No arguments passed")
        sys.exit(0)
    
    if args.name:
        results = cm.search_by_name(args.name)
        if not results:
            print_error(f"No contacts found with name '{args.name}'")
            sys.exit(0)
        headers = ["#", "Name", "Phone", "Email"]
        formatted_data = [
            [i, c.name, c.phone, c.email if c.email else "-"]
            for i,c in enumerate(results, start=1)
        ]
        print_table(formatted_data, headers)
        print()
        print_success(f"{len(results)} contact(s) found")
        sys.exit(0)
    if args.phone:
        results = cm.search_by_phone(args.phone)
        if not results:
            print_error(f"No contacts found with phone '{args.phone}'")
            sys.exit(0)
        headers = ["#", "Name", "Phone", "Email"]
        formatted_data = [
            [i, c.name, c.phone, c.email if c.email else "-"]
            for i,c in enumerate(results, start=1)
        ]
        print_table(formatted_data, headers)
        print()
        print_success(f"{len(results)} contact(s) found")
        sys.exit(0)
    
    if args.email:
        results = cm.search_by_email(args.email)
        if not results:
            print_error(f"No contacts found with email '{args.phone}'")
        headers = ["#", "Name", "Phone", "Email"]
        formatted_data = [
            [i, c.name, c.phone, c.email if c.email else "-"]
            for i,c in enumerate(results, start=1)
        ]
        print_table(formatted_data, headers)
        print()
        print_success(f"{len(results)} contact(s) found")
        sys.exit(0)
        
# Delete command
def cmd_delete(args):

    if not args:
        print("No arguments passed")
        sys.exit(0)

    try:
        result = cm.delete_contact(args.display_id)
        if result:
            print_success(f"Contact with display ID '{args.display_id}' deleted successfully")
            sys.exit(0)
        else:
            print_error("Command failed")
            sys.exit(1)
    except ValueError as e:
        print_error(e)
        sys.exit(1)

# Edit command
def cmd_edit(args):

    if not args:
        print("No arguments passed")
        sys.exit(0)

    try:
        # Validating inputs
        if args.name:
            validate(args.name, validate_name)
        if args.phone:
            validate(args.phone, validate_phone)
        if args.email:
            validate(args.email, validate_email)
        result = cm.edit_contact(
            args.display_id,
            name=args.name if args.name else None,
            phone=args.phone if args.phone else None,
            email=args.email if args.email else None
        )
        if result:
            print_success(f"Contact with display ID '{args.display_id}' updated successfully")
            sys.exit(0)
        else:
            print_error("Command failed")
            sys.exit(1)
    except ValueError as e:
        print_error(e)
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

    print_table(formatted_data, headers)
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

    # Search parser
    search_parser = sub.add_parser("search", help="Search in contacts using name, phone number or email")
    search_parser.add_argument("--name")
    search_parser.add_argument("--phone")
    search_parser.add_argument("--email")

    # Delete parser
    delete_parser = sub.add_parser("delete", help="Delete contact using display ID shown when list command run")
    delete_parser.add_argument("display_id", type=int)

    # Edit parser
    edit_parser = sub.add_parser("edit", help="Edit contact using display ID shown when list command run")
    edit_parser.add_argument("display_id", type=int)
    edit_parser.add_argument("--name")
    edit_parser.add_argument("--phone")
    edit_parser.add_argument("--email")

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
        
        elif args.command == "search":
            return cmd_search(args)
        
        elif args.command == "edit":
            return cmd_edit(args)

        elif args.command == "delete":
            return cmd_delete(args)

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