# Storage layer

# Libraries
from pathlib import Path
import json

# Project modules
from entity import Contact

# Project directories and files
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CONTACTS_FILE_PATH = DATA_DIR / "contacts.json"

# JSON Handler
class JSONFile:

    def __init__(self, FILE_PATH: Path):
        self.path = FILE_PATH

    def read_json(self, default=None):

        # Ensure file exists
        if not self.path.exists():
            return default
        
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, TypeError):
            return default
        
    def write_json(self, data: list[dict], indent: int=4):

        # Ensure directory exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent)
                return True
        except:
            return False

# Contacts DB
class ContactDB:

    def __init__(self, CONTACT_FILE=CONTACTS_FILE_PATH):
        self.json_handler = JSONFile(CONTACT_FILE)

    # Create file
    def create_file(self, data=[], indent=4) -> bool:

        # Check if exists
        if self.json_handler.path.exists():
            return True
        
        # Create if not
        self.json_handler.write_json(data, indent)
        return True
    
    # Add contact
    def add(self, contact: Contact) -> bool:

        # Convert to dict
        contact_dict = contact.to_dict()

        # Add to the file
        data = self.json_handler.read_json(default=[])
        data.append(contact_dict)
        self.json_handler.write_json(data)
        return True
    
    # Get all contacts
    def get_all(self) -> list[Contact]:

        # Read all data
        data = self.json_handler.read_json(default=[])

        # Converting to Contact objects
        contacts = [Contact.from_dict(c) for c in data]

        return contacts
    
    # Update contact
    def update(self, contact: Contact):

        # Read all
        data = self.json_handler.read_json(default=[])

        updated = False
        for i, contact in enumerate(data):
            if data["id"] == contact.id:
                data[i] = contact.to_dict()
                updated = True
                break

        if updated:
            self.json_handler.write_json(data)

        return updated
    
    # Delete contact
    def delete(self, contact: Contact):

        # Read all
        data = self.json_handler.read_json(default=[])

        # Filtered data
        filtered = [c for c in data if c["id"] != contact.id]

        if len(data) == len(filtered):
            return False
        
        # Write filtered
        self.json_handler.write_json(filtered)
        return True



if __name__ == "__main__":
    # j = JSONFile(CONTACTS_FILE_PATH)
    # print(j.write_json([]))
    # print(DATA_DIR)
    c = ContactDB()
    # # print(c.create_file())
    # # print(c.add(Contact("Saron", +919999947999)))
    # cs = c.get_all()
    # for i in cs:
    #     print(i)