from tkinter import ttk

class Dashboard:
    def __init__(self, root, username):
        root.title("Utilities Dashboard")
        root.geometry("800x550")
        root.resizable(True, True)

        ttk.Label(root, text=f"Logged in as: {username}").pack(anchor="e", padx=10, pady=5)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        for name in ("URL Shortener", "SMS & Email", "Fake Data Generator"):
            tab = ttk.Frame(notebook)
            ttk.Label(tab, text=f"{name} - coming soon").pack(pady=40)
            notebook.add(tab, text=name)