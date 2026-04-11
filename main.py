# Contact Manager CLI

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

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Initialize Contact Manager
cm = ContactManager(CONTACT_FILE=CONTACT_FILE_PATH)

# ========== UI UTILITIES ==========

init(autoreset=True)


def print_error(msg):
    """Print error message in red"""
    print(Fore.RED + f"✗ {msg}")


def print_success(msg):
    """Print success message in green"""
    print(Fore.GREEN + f"✓ {msg}")


def print_info(msg):
    """Print info message"""
    print(Fore.CYAN + f"ℹ {msg}")


def validate(arg, method, field_name):
    """Check validations and print error if invalid"""
    is_valid, error_msg = method(arg)
    if not is_valid:
        print_error(f"{field_name}: {error_msg}")
        return False
    return True


def print_table(data: list[list], headers: list):
    """Print formatted table"""
    from tabulate import tabulate
    print(tabulate(data, headers=headers, tablefmt="grid"))


# ========== COMMANDS ==========

def cmd_add(args):
    """Add a new contact"""
    try:
        # Validate inputs
        if not validate(args.name, validate_name, "Name"):
            return 1
        if not validate(args.phone, validate_phone, "Phone"):
            return 1
        if args.email:
            if not validate(args.email, validate_email, "Email"):
                return 1
        
        # Add contact
        result = cm.add_contact(name=args.name, phone=args.phone, email=args.email)
        
        if result:
            print_success(f"Contact '{args.name}' added successfully")
            return 0
        else:
            print_error("Failed to add contact")
            return 1
            
    except Exception as e:
        print_error(f"Error: {e}")
        return 1


def cmd_search(args):
    """Search contacts by name, phone, or email"""
    try:
        results = None
        search_term = None
        
        # Determine search type
        if args.name:
            results = cm.search_by_name(args.name)
            search_term = f"name '{args.name}'"
        elif args.phone:
            results = cm.search_by_phone(args.phone)
            search_term = f"phone '{args.phone}'"
        elif args.email:
            results = cm.search_by_email(args.email)
            search_term = f"email '{args.email}'"
        else:
            print_error("Provide --name, --phone, or --email")
            return 1
        
        # Display results
        if not results:
            print_info(f"No contacts found with {search_term}")
            return 0
        
        headers = ["#", "Name", "Phone", "Email"]
        formatted_data = [
            [i, c.name, c.phone, c.email if c.email else "-"]
            for i, c in enumerate(results, start=1)
        ]
        
        print(f"\n🔍 Search results for {search_term}:\n")
        print_table(formatted_data, headers)
        print()
        print_success(f"Found {len(results)} contact(s)")
        return 0
        
    except Exception as e:
        print_error(f"Error: {e}")
        return 1


def cmd_delete(args):
    """Delete a contact by display ID"""
    try:
        result = cm.delete_contact(args.display_id)
        
        if result:
            print_success(f"Contact #{args.display_id} deleted successfully")
            return 0
        else:
            print_error(f"Contact #{args.display_id} not found")
            return 1
            
    except ValueError as e:
        print_error(str(e))
        return 1
    except Exception as e:
        print_error(f"Error: {e}")
        return 1


def cmd_edit(args):
    """Edit a contact by display ID"""
    try:
        # Validate provided inputs
        if args.name:
            if not validate(args.name, validate_name, "Name"):
                return 1
        if args.phone:
            if not validate(args.phone, validate_phone, "Phone"):
                return 1
        if args.email:
            if not validate(args.email, validate_email, "Email"):
                return 1
        
        # Check if any field provided
        if not any([args.name, args.phone, args.email]):
            print_error("Provide at least one field to update: --name, --phone, or --email")
            return 1
        
        # Update contact
        result = cm.edit_contact(
            args.display_id,
            name=args.name if args.name else None,
            phone=args.phone if args.phone else None,
            email=args.email if args.email else None
        )
        
        if result:
            print_success(f"Contact #{args.display_id} updated successfully")
            return 0
        else:
            print_error(f"Contact #{args.display_id} not found")
            return 1
            
    except ValueError as e:
        print_error(str(e))
        return 1
    except Exception as e:
        print_error(f"Error: {e}")
        return 1


def cmd_list():
    """List all contacts"""
    try:
        contacts = cm.list_all()
        
        if not contacts:
            print_info("No contacts yet")
            print('Add one using: python main.py add --name "John" --phone 9876543210\n')
            return 0
        
        headers = ["#", "Name", "Phone", "Email"]
        formatted_data = [
            [c[0], c[2], c[3], c[4] if c[4] else "-"]
            for c in contacts
        ]
        
        print("\n📇 All Contacts\n")
        print_table(formatted_data, headers)
        print()
        print_success(f"Total {len(contacts)} contact(s)\n")
        return 0
        
    except Exception as e:
        print_error(f"Error: {e}")
        return 1


def cmd_help():
    """Show help information"""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║              CONTACT MANAGER - Help                            ║
╚════════════════════════════════════════════════════════════════╝

COMMANDS:
  add       Add a new contact (name and phone required)
  list      List all contacts
  search    Search contacts by name, phone, or email
  edit      Edit a contact using display ID
  delete    Delete a contact using display ID
  help      Show this help message

USAGE:
  python main.py <command> [options]

EXAMPLES:
  # Add contact
  python main.py add --name "Trisha Varma" --phone 9756843959 --email trish@gmail.com
  python main.py add --name "John Doe" --phone 9988776655

  # List all contacts
  python main.py list

  # Search contacts
  python main.py search --name Trisha
  python main.py search --phone 8844995533
  python main.py search --email vks@gmail.com

  # Edit contact (use display ID from list command)
  python main.py edit 1 --name "Trisha Varma"
  python main.py edit 2 --phone 9949944999 --email trish12@gmail.com

  # Delete contact
  python main.py delete 1

  # Show help
  python main.py help

VALIDATION RULES:
  Name:  2-50 characters, letters and spaces only
  Phone: 10 digits
  Email: Valid email format (optional)

DATA LOCATION:
  Contacts stored in: data/contacts.json
"""
    print(help_text)
    return 0


# ========== MAIN ==========

def main():
    """Main CLI entry point"""
    # Argument parser
    parser = argparse.ArgumentParser(
        prog="Contact Manager",
        description="Manage your contacts from the command line",
        add_help=False  # We handle help ourselves
    )
    
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # Add parser
    add_parser = sub.add_parser("add", help="Add contact")
    add_parser.add_argument("--name", required=True, help="Contact name")
    add_parser.add_argument("--phone", required=True, help="Phone number (10 digits)")
    add_parser.add_argument("--email", help="Email address (optional)")

    # Search parser
    search_parser = sub.add_parser("search", help="Search contacts")
    search_parser.add_argument("--name", help="Search by name")
    search_parser.add_argument("--phone", help="Search by phone")
    search_parser.add_argument("--email", help="Search by email")

    # Delete parser
    delete_parser = sub.add_parser("delete", help="Delete contact")
    delete_parser.add_argument("display_id", type=int, help="Display ID from list command")

    # Edit parser
    edit_parser = sub.add_parser("edit", help="Edit contact")
    edit_parser.add_argument("display_id", type=int, help="Display ID from list command")
    edit_parser.add_argument("--name", help="New name")
    edit_parser.add_argument("--phone", help="New phone")
    edit_parser.add_argument("--email", help="New email")

    # List parser
    list_parser = sub.add_parser("list", help="List all contacts")

    # Help parser
    help_parser = sub.add_parser("help", help="Show help")

    # Execute
    try:
        # Show help if no command
        if len(sys.argv) == 1:
            cmd_help()
            return 0
        
        args = parser.parse_args()
        
        # Route to command
        if args.command == "add":
            return cmd_add(args)
        elif args.command == "list":
            return cmd_list()
        elif args.command == "search":
            return cmd_search(args)
        elif args.command == "edit":
            return cmd_edit(args)
        elif args.command == "delete":
            return cmd_delete(args)
        elif args.command == "help":
            return cmd_help()
        else:
            print_error("Unknown command")
            cmd_help()
            return 1

    except KeyboardInterrupt:
        print("\n")
        print_info("Operation cancelled by user")
        return 130
        
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)