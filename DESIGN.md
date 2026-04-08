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
        "phone": +1 9428402380,
        "email": "jonathan.majors@gmail.com"
    },
    ...
]
```
- **Constraints**  
    - ID: Mandatory, uuid4  
    - Name: Mandatory, max 50 chars  
    - Phone: Mandatory, Country code + 10 digit number   
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
    - `search_by_phone(phone)` -> Contact

## CLI layer
- Methods
    - `cmd_add`
    - `cmd_list`
    - `cmd_help`