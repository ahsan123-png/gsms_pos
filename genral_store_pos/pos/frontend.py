import tkinter as tk
from tkinter import messagebox
import requests


# ========= fetch frontend API =============
def addEmployees():
    url='http://127.0.0.1:8000/users/add_users'
    data={
        "first_name": firstName.get(),
        "last_name":LastName.get() ,
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
            messagebox.showerror('Error', result.get('error','Something went wrong.'))
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error',f'An internal error {e}')
          
