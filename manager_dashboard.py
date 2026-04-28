import tkinter as tk
from tkinter import messagebox, simpledialog
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
            # Remove EVERYTHING from the login screen
            label.pack_forget()
            SSN_label.pack_forget()
            SSN_entry.pack_forget()
            # This line hides the "Login" button specifically
            for widget in root.winfo_children():
                if isinstance(widget, tk.Button) and widget['text'] == "Login":
                    widget.pack_forget()
            
            # Add the button to trigger your 'add_hotel_db' function
            tk.Button(root, text="Add New Hotel", command=add_hotel_db, width=30).pack(pady=20)
            tk.Button(root, text="Update Hotel Name", command=update_hotel_db, width=30).pack(pady=5)
            tk.Button(root, text="Remove Hotel", command=remove_hotel_db, width=30).pack(pady=5)
            tk.Button(root, text="View All Hotels", command=view_all_hotels, width=30).pack(pady=5)


        else:
            
            cur.close()
            conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def add_hotel_db():
    name = simpledialog.askstring("Input", "Hotel Name:")
    street = simpledialog.askstring("Input", "Street Name:")
    num = simpledialog.askstring("Input", "Street Number:")
    city = simpledialog.askstring("Input", "City:")    
    
    if name and street and num and city:
        try:
            conn = get_connection()
            cur = conn.cursor()
            # Add the Address first (ON CONFLICT prevents errors if the address already exists)
            cur.execute("""
                INSERT INTO Address (street_name, street_number, city) 
                VALUES (%s, %s, %s) 
                ON CONFLICT DO NOTHING
            """, (street, num, city)) 
            #  Now add the Hotel
            cur.execute("""
                INSERT INTO Hotel (name, street_name, street_number, city) 
                VALUES (%s, %s, %s, %s)
            """, (name, street, num, city))
            
            conn.commit()
            messagebox.showinfo("Success", f"Hotel '{name}' added successfully!")
            
            cur.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not add hotel: {e}")
        

def update_hotel_db():
    hotel_id = simpledialog.askinteger("Update", "Enter Hotel ID to update:")
    new_name = simpledialog.askstring("Update", "Enter new Hotel Name:")
    if hotel_id and new_name:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE Hotel SET name = %s WHERE hotel_id = %s", (new_name, hotel_id))
            conn.commit()
            messagebox.showinfo("Success", "Hotel updated successfully!")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")
            
def remove_hotel_db():
    hotel_id = simpledialog.askinteger("Remove", "Enter Hotel ID to remove:")
    if hotel_id:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM Hotel WHERE hotel_id = %s", (hotel_id,))
            conn.commit()
            messagebox.showinfo("Success", "Hotel removed successfully!")
            cur.close(); conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Removal failed: {e}")
            
def view_all_hotels():
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Grab ID, Name, and City so you can see which is which
        cur.execute("SELECT hotel_id, name, city FROM Hotel")
        hotels = cur.fetchall()
        
        if not hotels:
            messagebox.showinfo("Hotels", "No hotels found in the system.")
            return

        # Format the list so it's easy to read
        output = "ID | Name | City\n" + "-"*30 + "\n"
        for h in hotels:
            output += f"{h[0]} | {h[1]} | {h[2]}\n"
        
        messagebox.showinfo("All Hotels", output)
        cur.close(); conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch hotels: {e}")

         
        
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


