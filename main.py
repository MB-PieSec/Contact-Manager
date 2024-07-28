import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from contact_manager import ContactManager

class ContactManagerGUI:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Manager")
        
        self.create_widgets()
        self.apply_dark_mode()
        self.update_contacts_list()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.contact_listbox = tk.Listbox(self.main_frame, height=15, width=50)
        self.contact_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        self.add_button = ttk.Button(self.main_frame, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.delete_button = ttk.Button(self.main_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))

        self.info_button = ttk.Button(self.main_frame, text="Contact Info", command=self.contact_info)
        self.info_button.grid(row=2, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.update_button = ttk.Button(self.main_frame, text="Update Contact", command=self.update_contact)
        self.update_button.grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.search_button = ttk.Button(self.main_frame, text="Search Contact", command=self.search_contact)
        self.search_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.go_back)
        self.back_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        self.back_button.grid_remove()  

        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def apply_dark_mode(self):
        style = ttk.Style()
        
        # General settings for the dark theme
        style.theme_use("clam")
        style.configure("TFrame", background="#2e2e2e")
        style.configure("TButton", background="#3c3c3c", foreground="white", borderwidth=1)
        style.map("TButton", background=[("active", "#505050")])
        style.configure("TLabel", background="#2e2e2e", foreground="white")
        style.configure("TEntry", fieldbackground="#3c3c3c", foreground="white", borderwidth=1)
        style.configure("TCombobox", fieldbackground="#3c3c3c", foreground="white", background="#3c3c3c")
        style.configure("TListbox", background="#3c3c3c", foreground="white")
        
        # Update widget backgrounds
        self.root.configure(bg="#2e2e2e")
        self.main_frame.configure(style="TFrame")
        self.contact_listbox.configure(bg="#3c3c3c", fg="white", selectbackground="#505050")
        
    def update_contacts_list(self):
        self.contact_listbox.delete(0, tk.END)
        for name in self.manager.contacts.keys():
            self.contact_listbox.insert(tk.END, name)
    
    def add_contact(self):
        name = simpledialog.askstring("Add Contact", "Enter name:")
        if not name:
            return
        if name == None:
            return
        
        if name in self.manager.contacts:
            messagebox.showerror("Error", "This contact already exists.")
            return
        
        phone = simpledialog.askstring("Add Contact", "Enter phone:")
        if phone == None:
            return
        email = simpledialog.askstring("Add Contact", "Enter email (optional):")
        if email == None:
            return
        address = simpledialog.askstring("Add Contact", "Enter address (optional):")
        if address == None:
            return
        
        self.manager.add_contact(name, phone, email, address)
        self.update_contacts_list()
    
    def delete_contact(self):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if not selected_contact:
            messagebox.showerror("Error", "No contact selected.")
            return
        
        if messagebox.askyesno("Delete Contact", f"Are you sure you want to delete {selected_contact}?"):
            self.manager.delete_contact(selected_contact)
            self.update_contacts_list()
    
    def update_contact(self):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if not selected_contact:
            messagebox.showerror("Error", "No contact selected.")
            return
        
        phone = simpledialog.askstring("Update Contact", "Enter new phone:", initialvalue=self.manager.contacts[selected_contact]["phone"])
        if phone is None:
            return  

        email = simpledialog.askstring("Update Contact", "Enter new email (optional):", initialvalue=self.manager.contacts[selected_contact].get("email"))
        if email is None:
            return  

        address = simpledialog.askstring("Update Contact", "Enter new address (optional):", initialvalue=self.manager.contacts[selected_contact].get("address"))
        if address is None:
            return  
        
        rename = messagebox.askquestion("Update Contact", "Do you want to rename this contact?")
        if rename == 'yes':
            new_name = simpledialog.askstring("Update Contact", "Enter new name:", initialvalue=selected_contact)
            if new_name is None:
                return  
            self.manager.contacts[new_name] = self.manager.contacts.pop(selected_contact)
            selected_contact = new_name
        
        self.manager.update_contact(selected_contact, phone, email, address)
        self.update_contacts_list()
    
    def search_contact(self):
        query = simpledialog.askstring("Search Contact", "Enter name to search:")
        if not query:
            return
        
        found_contacts = [name for name in self.manager.contacts if query.lower() in name.lower()]
        self.contact_listbox.delete(0, tk.END)
        if not found_contacts:
            messagebox.showinfo("Search Contact", "No matching contacts found.")
        else:
            for name in found_contacts:
                self.contact_listbox.insert(tk.END, name)
        
        self.back_button.grid()  
    
    def go_back(self):
        self.update_contacts_list()  
        self.back_button.grid_remove()  
    
    def contact_info(self):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if not selected_contact:
            messagebox.showerror("Error", "No contact selected.")
            return
        
        info = self.manager.contacts[selected_contact]
        messagebox.showinfo("Contact Info", f"Name: {selected_contact}\nPhone: {info['phone']}\nEmail: {info.get('email')}\nAddress: {info.get('address')}")





if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerGUI(root)
    root.mainloop()
