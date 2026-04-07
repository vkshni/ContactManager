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
PROJECT_DIR = # Path
DATA_DIR = # Path
CONTACTS_FILE_PATH = # Path
```
- Classes and methods
    - JSONFile:
        - read_json(default=None) -> list[dict]
        - write_json(data, indent=4) -> bool

    - ContactDB:
        - self.json_handler (JSONFile)
        - setup(data, indent=4) -> bool
        - add(contact: Contact) -> bool
        - get_all() -> list[Contact]
        - delete(contact: Contact) -> bool
        - edit(contact: Contact) -> bool

## Entity layer
- Classes and methods   
    - __init__(self, name, phone, email=None, id=None)
    - `@classmethod` from_dict(cls, contact_dict) -> bool
    - to_dict(self) -> dict

- Validators
    - validate_name(name)
    - validate_phone(phone)
    - validate_email(email)

    