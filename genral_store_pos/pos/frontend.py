import tkinter as tk
from tkinter import messagebox
import requests

#========== clear screens =============
def clear_fields():
    firstName.delete(0, tk.END)
    lastName.delete(0, tk.END)
    email.delete(0, tk.END)
    password.delete(0, tk.END)
    designation.delete(0, tk.END)
    gender.delete(0, tk.END)
    phoneNumber.delete(0, tk.END)
# ========= fetch frontend API =============
def addEmployees():
    url='http://127.0.0.1:8000/users/add_users'
    data={
        "first_name": firstName.get(),
        "last_name":lastName.get() ,
        "password":password.get() ,
        "designation":designation.get() ,
        "gender":gender.get() ,
        "phoneNumber":phoneNumber.get() ,
        "email":email.get() 
        }
    try:
        response=requests.post(url,json=data)
        result=response.json()
        if response.status_code==200:
            if 'success' in result:
                messagebox.showinfo('Success', 'Employee added successfully!')
                clear_fields() 
            else:
                messagebox.showerror('Error', result.get('error','Something went wrong.'))
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error',f'An internal error {e}')
          



# =========== UI with tkinter ================
main=tk.Tk()
main.title('POS System')
tk.Label(main,text="Add New Employee").grid(row=0,column=0,columnspan=2)

tk.Label(main,text='First Name').grid(row=1,column=0)
firstName=tk.Entry(main)
firstName.grid(row=1,column=1)

tk.Label(main, text="Last Name").grid(row=2, column=0)
lastName = tk.Entry(main)
lastName.grid(row=2, column=1)

tk.Label(main, text="Email").grid(row=3, column=0)
email = tk.Entry(main)
email.grid(row=3, column=1)

tk.Label(main, text="Password").grid(row=4, column=0)
password = tk.Entry(main, show='*')
password.grid(row=4, column=1)

tk.Label(main, text="Designation").grid(row=5, column=0)
designation = tk.Entry(main)
designation.grid(row=5, column=1)

tk.Label(main, text="Gender").grid(row=6, column=0)
gender = tk.Entry(main)
gender.grid(row=6, column=1)

tk.Label(main, text="Phone Number").grid(row=7, column=0)
phoneNumber = tk.Entry(main)
phoneNumber.grid(row=7, column=1)

tk.Button(main, text="Add Employee", command=addEmployees).grid(row=8, column=0, columnspan=2)

main.mainloop()
