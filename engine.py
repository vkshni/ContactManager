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
        existing = self.phone_exists(phone)
        if existing:
            raise ValueError(f"Contact with phone {phone} already exists")

        # Creating Contact object
        contact = Contact(name, phone, email=email)
        
        # Adding using db
        self.contact_db.add(contact)
        return True

    # check if phone number exists
    def phone_exists(self, phone: str):

        contacts = self.contact_db.get_all()
        for contact in contacts:
            if phone == contact.phone:
                return True
            
        return False
            
    # Search by phone
    def search_by_phone(self, phone: str) -> Contact:


        contacts = self.contact_db.get_all()
        searches = [contact for contact in contacts if phone in contact.phone]
        return searches
    
    # Search by name
    def search_by_name(self, name: str) -> list[Contact]:

        contacts = self.contact_db.get_all()

        searches = [contact for contact in contacts if name.lower() in contact.name.lower()]
        return searches
    
    # Search by email
    def search_by_email(self, email: str) -> list[Contact]:
    
        contacts = self.contact_db.get_all()

        searches = [contact for contact in contacts if contact.email and email.lower() in contact.email.lower()]
        return searches
            
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
    
    # Get display id
    def get_contact_by_display_id(self, display_id: int) -> Contact | None:

        # Get all contacts(numbered)
        contacts = self.contact_db.get_all()

        if 0 < display_id <= len(contacts):
            return contacts[display_id-1]
        
        return None
            
    # Delete contact
    def delete_contact(self, display_id: int) -> bool:

        contact = self.get_contact_by_display_id(display_id)

        if not contact:
            raise ValueError(f"Contact with display ID '{display_id}' not found")
        
        self.contact_db.delete(contact)
        return True
    
    # Edit contact
    def edit_contact(self, display_id: int, **kwargs) -> bool:

        contact = self.get_contact_by_display_id(display_id)

        if not contact:
            raise ValueError(f"Contact with display ID '{display_id}' not found")
        
        if kwargs.get("name"):
            contact.name = kwargs["name"]
        if kwargs.get("phone"):
            contact.phone = kwargs["phone"]
        if kwargs.get("email"):
            contact.email = kwargs["email"]

        # Write to db
        self.contact_db.update(contact)
        return True


if __name__ == "__main__":

    cm = ContactManager()
    # print(cm.add_contact("Reman", "+91 937483748"))
    # print(cm.search_by_phone("34"))
    all_contacts = cm.list_all()
    for c in all_contacts:
        print(c)
    # searches = cm.search_by_name("v")
    # for s in searches:
    #     print(s)
    # searches = cm.search_by_email("riya")
    # for s in searches:
    #     print(s)

    # print(cm.delete_contact(2))
    # print(cm.edit_contact(4, name="Riya Singh", phone="9999998888", email="riyasingh@gmail.com"))