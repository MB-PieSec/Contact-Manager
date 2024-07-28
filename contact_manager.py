import json
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    filename="contacts_log.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def save_file_decorator(func):
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.save_file()
        return result
    return wrapper

class ContactManager:
    def __init__(self):
        self.contacts = {}
        self.index_to_name = {}
        try:
            with open("contacts.json", "r") as file:
                self.contacts = json.load(file)
        except FileNotFoundError:
            logging.info("No contacts.json file found. Creating a new one...")
            self.save_file()
    
    def save_file(self):
        with open("contacts.json", "w") as file:
            json.dump(self.contacts, file, indent=4)
    
    @save_file_decorator
    def add_contact(self, name, phone, email=None, address=None):
        self.contacts[name] = {"phone": phone, "email": email, "address": address}
        logging.info(f"Contact: {name} - added successfully.")
        print(f"Contact: {name} - added successfully.")
    
    @save_file_decorator
    def delete_contact(self, name):
        try:
            del self.contacts[name]
            logging.info(f"Contact: {name} - was deleted successfully.")
            print(f"Contact: {name} - was deleted successfully.")
        except KeyError:
            print("Contact not found. Please try again.")
            logging.warning("Attempt to delete a non-existent contact.")
    
    @save_file_decorator
    def update_contact(self, name, phone, email=None, address=None):
        if name in self.contacts:
            self.contacts[name]["phone"] = phone
            if email:
                self.contacts[name]["email"] = email
            if address:
                self.contacts[name]["address"] = address
            logging.info(f"Contact: {name} - was updated successfully.")
            print(f"Contact: {name} - was updated successfully.")
        else:
            print("Contact not found. Please try again.")
            logging.warning("Attempt to update a non-existent contact.")
    
    def search_contact(self, query):
        while True:
            found = [name for name in self.contacts if query in name]
            if found:
                for name in found:
                    print(f"{name}: {self.contacts[name]}")
            else:
                print("No matching contacts found.")
            
            re_search = input("Do you want to search again? (y/n): ")
            if re_search.lower() == "y":
                query = input("Search contact: ")
            else:
                break
    
    def contact_info(self):
        while True:
            user_input = input("Enter contact index to see info or [m] to return to menu: ")
            if user_input.lower() == "m":
                return
            try:
                index = int(user_input)
                if index in self.index_to_name:
                    contact_name = self.index_to_name[index]
                    contact_info = self.contacts[contact_name]
                    print(f"Contact info for {contact_name}: {contact_info}")
                else:
                    print("Invalid index!")
            except ValueError:
                print("Invalid input! Please enter a valid index or 'm' to return to menu.")
    
    def contacts_list(self):
        self.index_to_name = {i + 1: name for i, name in enumerate(self.contacts)}
        for i, name in self.index_to_name.items():
            print(f"{i}. {name} - [Enter {i} for contact info]")
        
        while True:
            update_info = input("Press 'i' to see contact info or 'u' to update any contacts, 'm' to return to menu: ")
            if update_info.lower() == "i":
                self.contact_info()
                break
            elif update_info.lower() == "u":
                self.update_contact()
                break
            elif update_info.lower() == "m":
                break
            else:
                print("Invalid input!")
    
    def menu(self):
        options = {
            1: self.add_contact_menu,
            2: self.delete_contact_menu,
            3: self.contacts_list,
            4: self.search_contact_menu,
            5: self.exit_program
        }
        
        while True:
            print("1. Add Contact\n2. Delete Contact\n3. Contacts List\n4. Search Contacts\n5. Exit")
            try:
                user_input = int(input("Please select 1, 2, 3, 4 or 5: "))
                if user_input in options:
                    options[user_input]()
                else:
                    print("Invalid input...")
            except ValueError:
                print("Please enter the correct value!\nReturning to menu...")
                time.sleep(0.5)
    
    def add_contact_menu(self):
        name = input("Enter name: ")
        if name in self.contacts:
            print("This contact already exists.")
        else:
            phone = input("Enter phone: ")
            email = input("Enter email (Optional): ")
            address = input("Enter address (Optional): ")
            self.add_contact(name, phone, email, address)
    
    def delete_contact_menu(self):
        name = input("Enter name: ")
        if name not in self.contacts:
            print("Contact is not on the list!")
            logging.info("Attempt to delete a non-existent contact.")
        else:
            self.delete_contact(name)
    
    def search_contact_menu(self):
        user_query = input("Search contact: ")
        self.search_contact(user_query)
    
    def exit_program(self):
        print("Exiting...")
        time.sleep(0.5)
        exit()

if __name__ == "__main__": 
    contact_manager = ContactManager()
    contact_manager.menu()
