# Service layer

# Project modules
from entity import Contact
from storage import ContactDB, CONTACTS_FILE_PATH



# Contact Manager
class ContactManager:

    def __init__(self, CONTACT_FILE=CONTACTS_FILE_PATH):

        self.contact_db = ContactDB(CONTACT_FILE)

    # Add contact
    def add_contact(self, name: str, phone: str, email: str=None) -> bool:

        # Check if phone exists or not
        existing = self.search_by_phone(phone)
        if existing:
            raise ValueError(f"Contact with phone {phone} already exists")

        # Creating Contact object
        contact = Contact(name, phone, email=email)
        
        # Adding using db
        self.contact_db.add(contact)
        return True

    # Search by phone
    def search_by_phone(self, phone: str) -> Contact:

        contacts = self.contact_db.get_all()

        for contact in contacts:
            if phone in contact.phone:
                return contact
            
    # List all contacts
    def list_all(self) -> list[list]:

        # Get all contacts
        contacts = self.contact_db.get_all()

        # Numbered contacts
        numbered = [
            [idx] + contact.to_list()
            for idx, contact in enumerate(contacts, start=1)
            ]
        
        return numbered
            
if __name__ == "__main__":

    cm = ContactManager()
    # print(cm.add_contact("Reman", "+91 937483748"))
    # print(cm.search_by_phone("34"))
    all_contacts = cm.list_all()
    for c in all_contacts:
        print(c)