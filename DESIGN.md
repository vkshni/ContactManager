# DESIGN DOCUMENT

## Directory Structure
```bash
--ContactManager/
    --main.py   (CLI)
    --storage.py (Storage layer)
    --entity.py (Entity layer)
    --engine.py (Service layer)
    --data/
        --contacts.json
    --README.md
    --DESIGN.md
    --PLAN.md
```

## Data Storage
- JSON file format
```bash
[
    {
        "id":"49438sdj-8wj48-sdj9",
        "name": "Jonathan Majors"
        "phone": "9428402380",
        "email": "jonathan.majors@gmail.com"
    },
    ...
]
```
- **Constraints**  
    - ID: Mandatory, uuid4  
    - Name: Mandatory, max 50 chars  
    - Phone: Mandatory, 10 digit string  
    - Email: Optional, valid email

## Features
- Add contacts
- View All contacts
- Search contacts (`name`,`phone`,`email`)
- Delete contact
- Edit contact (`name`,`phone`,`email`)

## Storage layer
- Directories and file paths
```python
PROJECT_ROOT = # Path
DATA_DIR = # Path
CONTACTS_FILE_PATH = # Path
```
- Classes and methods
    - JSONFile:
        - `read_json(default=None)` -> list[dict]
        - `write_json(data, indent=4)` -> bool

    - ContactDB:
        - `self.json_handler` (JSONFile)
        - `create_file(data=[], indent=4)` -> bool
        - `add(contact: Contact)` -> bool
        - `get_all()` -> list[Contact]
        - `delete(contact: Contact)` -> bool
        - `edit(contact: Contact)` -> bool

## Entity layer
- Class `Contact`  
    - `__init__(name, phone, email=None, id=None)`
    - *`@classmethod`* `from_dict(cls, contact_dict)` -> Contact
    - `to_dict()` -> dict
    - `to_list()` -> list

- Validators
    - `validate_name(name)` -> (bool, error_msg)
    - `validate_phone(phone)` -> (bool, error_msg)
    - `validate_email(email)` -> (bool, error_msg)

## Service layer
- Class `ContactManager`
    - `add_contact(name, phone, emali=None)` -> bool
    - `list_all()` -> list[Contact]
    - `phone_exists(phone)` -> bool
    - `search_by_phone(phone)` -> Contact
    - `search_by_name(name)` -> Contact
    - `search_by_email(name)` -> Contact
    - `get_display_id(contact)` -> int
    - `delete_contact(display_id)` -> bool
    - `edit_contact(display_id, **kwargs)` -> bool

## CLI layer
- Methods
    - `cmd_add()` - `add` command
    - `cmd_search()` - `search` command (search by name, phone or email)
    - `cmd_delete()` - `delete` command (using display ID)
    - `cmd_edit()` - `edit` command (using display ID)
    - `cmd_list()` - `list` command
    - `cmd_help()` - `help` command
    - `run()` - Main argument parser and excecution