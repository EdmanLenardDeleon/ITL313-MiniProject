import tkinter as tk
from tkinter import ttk, messagebox
from auth import register_user, login_user

class LoginApp:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        root.title("Login")
        root.geometry("320x280")
        root.resizable(False, False)

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Welcome", font=("Segoe UI", 16, "bold")).pack(pady=(0, 15))
        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username = ttk.Entry(frame)
        self.username.pack(fill="x", pady=(0, 8))
        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password = ttk.Entry(frame, show="*")
        self.password.pack(fill="x", pady=(0, 8))

        ttk.Button(frame, text="Login", command=self.login).pack(fill="x", pady=(10, 4))
        ttk.Button(frame, text="Register", command=self.register).pack(fill="x")
        root.bind("<Return>", lambda e: self.login())

    def login(self):
        user = self.username.get().strip()
        if login_user(user, self.password.get()):
            self.on_success(user)
        else:
            messagebox.showerror("Login failed", "Wrong username or password.")

    def register(self):
        ok, msg = register_user(self.username.get().strip(), self.password.get())
        (messagebox.showinfo if ok else messagebox.showerror)("Register", msg)