# Entity layer

# Libraries
from uuid import uuid4

# Contact
class Contact:

    def __init__(self, name: str, phone: str, email: str=None, id: str=None):
        self.name = name
        self.phone = phone
        self.email = email
        self.id = str(id) if id else str(uuid4())

    def __str__(self):
        return f"Contact(name={self.name}, phone={self.phone}, email={self.email}, id={self.id})"
    
    def to_list(self):
        return [
            self.id,
            self.name,
            self.phone,
            self.email
        ]

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email
        }
    
    @classmethod
    def from_dict(cls, contact_dict: dict):
        
        return cls(
            name=contact_dict["name"],
            phone=contact_dict["phone"],
            email=contact_dict["email"],
            id=contact_dict["id"]
        )

# Validators
def validate_name(name: str):

    if not name or name.isspace() or not name.strip():
        return (False, f"Name cannot be empty")

def validate_phone(phone: int):
    pass

def validate_email(email: str):
    pass

if __name__ == "__main__":
    c1 = Contact("Sahani", +919538043838)
    print(c1)