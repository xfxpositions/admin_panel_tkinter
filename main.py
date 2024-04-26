import tkinter as tk
from utils.general import center_window
from ui.admin_panel import open_admin_panel_window
from utils.cryptomanager import CryptoManager

# Initialize the cryptomanager first
crypto_manager = CryptoManager()

# Create the main application window
root = tk.Tk()
root.title("My Tkinter Window")
root.geometry("300x300")
center_window(root)

# Create a button to open the admin panel
admin_button = tk.Button(
    root, text="Open Admin Panel", command=lambda: open_admin_panel_window(root)
)
admin_button.pack()

# Run the Tkinter event loop
root.mainloop()
