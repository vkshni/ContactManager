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


