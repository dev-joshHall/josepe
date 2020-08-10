import tkinter as tk
from bank_account import *

root = tk.Tk()
root.title('Josepe Bank (not a real bank)')



# set up labels
comp_name_label = tk.Label(master=root, text='Josepe Bank', fg='red', font=('Stylish', 44))
not_real_label = tk.Label(master=root, text='(not a real bank)', fg='red', font=('Stylish', 14))
username_label = tk.Label(master=root, text='Username: ', fg='black', font=('Courier', 14))
username_entry = tk.Entry(master=root)
password_label = tk.Label(master=root, text='Password: ', fg='black', font=('Courier', 14))
password_entry = tk.Entry(master=root)
login_button = tk.Button(master=root, text='Login', font=('Courier', 14))

# place labels
comp_name_label.grid(row=0, column=0, columnspan=3, padx=50, pady=5)
not_real_label.grid(row=1, column=0, columnspan=3, pady=5)
username_label.grid(row=2, column=0, padx=5, pady=5)
username_entry.grid(row=2, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
password_label.grid(row=3, column=0, padx=5, pady=5)
password_entry.grid(row=3, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
login_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
