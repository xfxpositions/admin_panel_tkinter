import tkinter as tk
from tkinter import ttk, messagebox
from utils.general import center_window
from ui.admin_panel import open_admin_panel_window
from utils.cryptomanager import CryptoManager

# Constants
ENTRANCE_PASSWORD = "deneme"


class LoginWindow:
    def __init__(self, parent):
        self.parent = parent
        self.login_window = tk.Toplevel(parent)
        self.setup_ui()
        self.login_window.grab_set()
        self.login_window.lift()

    def setup_ui(self):
        """Setup the login window UI components."""
        center_window(self.login_window)
        self.login_window.title("Admin Login")

        ttk.Label(self.login_window, text="Enter Password:").pack(pady=10)
        self.password_entry = ttk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)
        self.password_entry.focus_set()
        self.login_window.geometry("200x200")
        self.login_window.resizable(False, False)

        submit_button = ttk.Button(
            self.login_window, text="Submit", command=self.check_password
        )
        submit_button.pack(pady=10)
        self.password_entry.bind("<Return>", self.check_password)

    def check_password(self, event=None):
        """Check the entered password against the defined constant."""
        entered_password = self.password_entry.get()
        if entered_password == ENTRANCE_PASSWORD:
            self.login_window.destroy()
            open_admin_panel_window(self.parent)
        else:
            messagebox.showerror("Error", "Incorrect Password")
            self.password_entry.delete(
                0, "end"
            )  # Clear the input field for a new attempt


def setup_main_window():
    """Create and set up the main application window."""
    root = tk.Tk()
    root.title("My Tkinter Window")
    root.geometry("300x300")
    center_window(root)

    admin_button = ttk.Button(
        root, text="Open Admin Panel", command=lambda: LoginWindow(root)
    )
    admin_button.pack()

    root.mainloop()


# Initialize the cryptomanager
crypto_manager = CryptoManager()

# Run the main application window setup
if __name__ == "__main__":
    setup_main_window()
