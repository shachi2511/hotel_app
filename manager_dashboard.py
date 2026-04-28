import tkinter as tk
from tkinter import messagebox
from db import get_connection  


def login_action():
    ssn = SSN_entry.get()
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        
        cur.execute("SELECT name FROM Managers WHERE SSN = %s", (ssn,))
        result = cur.fetchone()
        if result:
            messagebox.showinfo("Login Success", f"Welcome, {result[0]}!")
        else:
            messagebox.showerror("Login Failed", "SSN not found in our records.")
            
            cur.close()
            conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        
        
#Main setup
root = tk.Tk()

root.title("Manager Dashboard")
root.geometry("400x400")



label = tk.Label(root, text="Hello! This is my Manager Project.")
label.pack()

SSN_label = tk.Label(root,text = "Enter SSN:")
SSN_label.pack()

SSN_entry = tk.Entry(root,width=30)
SSN_entry.pack()

tk.Button(root, text="Login", command=login_action).pack(pady=10)



root.mainloop()


