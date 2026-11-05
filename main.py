import tkinter as tk
from database import init_db
from login_gui import LoginApp
from dashboard import Dashboard

def start_dashboard(username):
    root.unbind("<Return>")
    for widget in root.winfo_children():
        widget.destroy()
    Dashboard(root, username)

init_db()
root = tk.Tk()
LoginApp(root, start_dashboard)
root.mainloop()