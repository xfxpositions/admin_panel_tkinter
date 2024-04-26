import tkinter as tk
from tkinter import ttk
from utils.general import center_window
from utils.secretsmanager import OpenAIConfig, SecretsManager


def open_admin_panel_window(root: tk.Tk):

    admin_panel = tk.Toplevel(root)
    admin_panel.title("Admin Panel")
    admin_panel.geometry("500x500")  # Adjusted for better spacing
    center_window(admin_panel)

    secrets_manager = SecretsManager()

    # Frame for API configurations
    config_frame = ttk.Frame(admin_panel, padding="10 10 10 10")
    config_frame.pack(fill="x", expand=True)

    # Labels and Entries
    ttk.Label(config_frame, text="Welcome to the Admin Panel").pack(pady=10)

    ttk.Label(config_frame, text="Deepgram API Key:").pack(anchor="w")
    deepgram_api_key_entry = ttk.Entry(config_frame)
    deepgram_api_key_entry.insert(0, secrets_manager.deepgram_api_key)
    deepgram_api_key_entry.pack(fill="x", padx=5, pady=5)

    # Combobox for selecting OpenAI configurations
    ttk.Label(config_frame, text="OpenAI Configs:").pack(anchor="w")
    openai_config_combobox = ttk.Combobox(config_frame, state="readonly")
    openai_config_names = [config.name for config in secrets_manager.openai_configs]
    openai_config_combobox["values"] = openai_config_names
    openai_config_combobox.pack(fill="x", padx=5, pady=5)
    if openai_config_names:
        openai_config_combobox.current(0)

    # Frame for buttons
    button_frame = ttk.Frame(admin_panel, padding="10 10 10 10")
    button_frame.pack(fill="x", expand=True)

    # Buttons
    ttk.Button(
        button_frame,
        text="Add New OpenAI Config",
        command=lambda: add_new_openai_config(),
    ).pack(side="left", expand=True, padx=5, pady=5)
    ttk.Button(
        button_frame,
        text="Update Secrets",
        command=lambda: update_secrets(),
    ).pack(side="left", expand=True, padx=5, pady=5)

    # Control Buttons
    control_frame = ttk.Frame(admin_panel, padding="10")
    control_frame.pack(fill="x", side="bottom", anchor="e")

    apply_button = ttk.Button(
        control_frame, text="Apply", command=lambda: apply_changes()
    )
    apply_button.pack(side="right", padx=5, pady=5)  # Changed side to "right"

    exit_button = ttk.Button(
        control_frame, text="Exit", command=lambda: admin_panel.destroy()
    )
    exit_button.pack(side="right", padx=5, pady=5)  # Changed side to "right"

    def apply_changes():
        # Function to apply changes
        print("Apply changes")

    def add_new_openai_config():
        new_config = OpenAIConfig("New Config", "", "", "", "", "")
        edit_openai_config(
            new_config, add=True
        )  # Pass new config to edit function with add flag

    def edit_openai_config(config, add=False):
        # Create a window for editing OpenAI config fields
        edit_window = tk.Toplevel(admin_panel)
        edit_window.title("Edit OpenAI Config")
        edit_window.geometry("400x300")
        center_window(edit_window)

        entry_fields = {}
        for attribute in vars(config):
            label = ttk.Label(edit_window, text=attribute.capitalize() + ":")
            label.pack()
            entry = ttk.Entry(edit_window, width=30)
            entry.insert(0, getattr(config, attribute))
            entry.pack()
            entry_fields[attribute] = entry

        def save_changes():
            for attribute, entry in entry_fields.items():
                setattr(config, attribute, entry.get())
            print("Changes saved for", config.name)
            if add:
                secrets_manager.add_openai_config(config)
            edit_window.destroy()

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes)
        save_button.pack()

    add_button = ttk.Button(
        admin_panel, text="Add New OpenAI Config", command=add_new_openai_config
    )
    add_button.pack()

    # Button to update secrets
    def update_secrets():
        # Update Deepgram API key
        new_deepgram_api_key = deepgram_api_key_entry.get()

        # Get the index of the selected OpenAI config
        openai_config_index = openai_config_combobox.current()

        # # Update JSON filename
        # secrets_manager.settings_filename = json_filename_entry.get()

        # Call SecretsManager method to update secrets
        secrets_manager.update_secrets(new_deepgram_api_key, openai_config_index)

        # Save settings to file after updating
        secrets_manager.to_json(secrets_manager.settings_filename)

    update_button = ttk.Button(
        admin_panel, text="Update Secrets", command=update_secrets, width=20
    )  # Make the button wider
    update_button.pack()


# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    open_admin_panel_window(root)
    root.mainloop()
