import tkinter as tk
import re
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import datetime
from bank_account import *
from admin import admin

login_attempts = 0
maggy = Customer('Maggy', 39, '1020 N 550 S Heber, UT', '9807593056', 'maggysmith@gmail.com', 'blabla', admin)
acc_1 = SavingsAccount(owners=[maggy], interest=.03, balance=300, minimum_bal=250, overdraft_fee=5,
                       withdrawal_lim=2, administration=admin)


def homepage_window(user):
    def sign_out():
        documents_button.image, accounts_button.image, settings_button.image, img_label.image = None, None, None, None
        login_page()

    root.title('Josepe Bank (not a real bank) - {}\'s profile'.format(user.name.split()[0]))
    for old_el in elements.values():
        old_el.grid_forget()
    img_1 = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/stack-of-manuals.png'))
    img_2 = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/accounts.jpg'))
    img_3 = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/settings.jpg'))
    img_4 = img_logo.resize((604, 180), Image.ANTIALIAS)
    img_4 = ImageTk.PhotoImage(img_4)
    img_label = tk.Label(master=root, image=img_4, padx=0)
    welcome_label = tk.Label(master=root, text='Welcome {}!'.format(user.name.split()[0]), bg='white', padx=5, pady=10,
                             anchor='w')
    signout_button = tk.Button(master=root, text='Sign out', command=sign_out)
    accounts_button = tk.Button(master=root, text='Accounts', image=img_2)
    documents_button = tk.Button(master=root, text='Documents', image=img_1)
    settings_button = tk.Button(master=root, text='Account Settings', image=img_3)
    documents_button.image, accounts_button.image, settings_button.image, img_label.image = img_1, img_2, img_3, img_4
    # grid elements
    img_label.grid(row=0, column=0, columnspan=2, sticky='nesw')
    welcome_label.grid(row=2, column=0, sticky='nesw')
    signout_button.grid(row=2, column=1, sticky='nes')
    accounts_button.grid(row=3, column=0, columnspan=2, sticky='nesw')
    documents_button.grid(row=4, column=0, columnspan=2, sticky='nesw')
    settings_button.grid(row=5, column=0, columnspan=2, sticky='nesw')
    elements['img label'] = img_label
    elements['welcome label'] = welcome_label
    elements['signout button'] = signout_button
    elements['accounts button'] = accounts_button
    elements['documents button'] = documents_button
    elements['settings button'] = settings_button


def new_user_window():
    def create_account():
        email = email_entry.get()
        password = pass_entry.get()
        confirmed_pass = confirm_pass_entry.get()
        name = name_entry.get()
        date_of_birth = DOB_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()
        # verify email
        email_pattern = re.compile(r'^([a-zA-Z0-9_\-.]+)@([a-zA-Z0-9_\-.]+)\.([a-zA-Z]{2,5})$')
        email_matches = email_pattern.finditer(email)
        if not [i for i in email_matches]:
            messagebox.showinfo(message='Not a valid email address')
            return -1
        # verify password
        if password == confirmed_pass:
            password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
            password_matches = password_pattern.finditer(password)
            if not [i for i in password_matches]:
                messagebox.showinfo(message='The password must contain:\n  - A number\n  - A lowercase letter\n  - An '
                                            'uppercase letter')
                return -1
        else:
            messagebox.showinfo(message='Password and Confirmed Password should be the same')
            return -1
        # verify date of birth
        date_pattern = re.compile(r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$')
        date_matches = date_pattern.finditer(date_of_birth)
        if not [i for i in date_matches]:
            messagebox.showinfo(message='Enter a valid date of birth (DD/MM/YYYY)')
            return -1
        # verify phone
        phone_pattern = re.compile(r'^[2-9]\d{2}-?\d{3}-?\d{4}$')
        password_matches = phone_pattern.finditer(phone)
        if not [i for i in password_matches]:
            messagebox.showinfo(message='Enter a valid phone number')
            return -1
        if not address:
            messagebox.showinfo(message='Enter an address')
            return -1
        date_of_birth = datetime.strptime(date_of_birth, '%m/%d/%Y')
        user = Customer(name, date_of_birth, address, phone, email, password, admin)
        homepage_window(user=user)

    def handle_focus_in(_):
        if DOB_entry.get() == 'MM/DD/YYYY':
            DOB_entry.delete(0, tk.END)
        DOB_entry.config(fg='black')

    def handle_focus_out(_):
        if len(DOB_entry.get()) == 0:
            DOB_entry.delete(0, tk.END)
            DOB_entry.config(fg='grey')
            DOB_entry.insert(0, 'MM/DD/YYYY')

    # clear old elements from screen
    for key, old_el in elements.items():
        if key != 'comp_logo':
            old_el.grid_forget()
    # create new elements
    email_label = tk.Label(master=root, text='Email address: ', font=('Courier', 14), bg='white')
    email_entry = tk.Entry(master=root, bg='#F0F0F0')
    pass_label = tk.Label(master=root, text='Password: ', font=('Courier', 14), bg='white')
    pass_entry = tk.Entry(master=root, bg='#F0F0F0')
    confirm_pass_label = tk.Label(master=root, text='Confirm password: ', font=('Courier', 14), bg='white')
    confirm_pass_entry = tk.Entry(master=root, bg='#F0F0F0')
    create_profile_button = tk.Button(text='Create profile', command=create_account)
    name_label = tk.Label(master=root, text='Full name: ', font=('Courier', 14), bg='white')
    name_entry = tk.Entry(master=root, bg='#F0F0F0')
    DOB_label = tk.Label(master=root, text='Date of Birth: ', font=('Courier', 14), bg='white')
    DOB_entry = tk.Entry(master=root, bg='#F0F0F0', fg='grey')
    phone_label = tk.Label(master=root, text='Phone number: ', font=('Courier', 14), bg='white')
    phone_entry = tk.Entry(master=root, bg='#F0F0F0')
    address_label = tk.Label(master=root, text='Address: ', font=('Courier', 14), bg='white')
    address_entry = tk.Entry(master=root, bg='#F0F0F0')
    # grid new elements
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry.grid(row=2, column=1, padx=15, pady=5, sticky='ew', columnspan=2)
    pass_label.grid(row=3, column=0, padx=5, pady=5)
    pass_entry.grid(row=3, column=1, padx=15, pady=5, sticky='ew', columnspan=2)
    confirm_pass_entry.grid(row=4, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
    confirm_pass_label.grid(row=4, column=0, padx=5, pady=5)
    name_label.grid(row=5, column=0, padx=5, pady=5)
    name_entry.grid(row=5, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
    DOB_label.grid(row=6, column=0, padx=5, pady=5)
    DOB_entry.grid(row=6, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
    phone_label.grid(row=7, column=0, padx=5, pady=5)
    phone_entry.grid(row=7, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
    address_label.grid(row=8, column=0, padx=5, pady=5)
    address_entry.grid(row=8, column=1, columnspan=2, padx=15, pady=5, sticky='ew')
    create_profile_button.grid(row=9, column=0, columnspan=3, padx=5, pady=5)
    DOB_entry.insert(0, 'MM/DD/YYYY')
    DOB_entry.bind("<FocusIn>", handle_focus_in)
    DOB_entry.bind("<FocusOut>", handle_focus_out)
    # add to elements dictionary
    elements['email label'] = email_label
    elements['email entry'] = email_entry
    elements['pass label'] = pass_label
    elements['pass entry'] = pass_entry
    elements['confirm label'] = confirm_pass_label
    elements['confirm entry'] = confirm_pass_entry
    elements['name label'] = name_label
    elements['name entry'] = name_entry
    elements['DOB label'] = DOB_label
    elements['DOB entry'] = DOB_entry
    elements['phone label'] = phone_label
    elements['phone entry'] = phone_entry
    elements['address label'] = address_label
    elements['address entry'] = address_entry
    elements['create button'] = create_profile_button


def login_page():
    def login_request():
        global login_attempts
        username_attempt = username_entry.get()
        password_attempt = password_entry.get()
        success, customer = admin.customer_login(username_attempt, password_attempt)
        if login_attempts >= 2:
            messagebox.showinfo(message='Too many login attempts')
        elif username_attempt.strip() == '':
            messagebox.showinfo(message='Username field empty')
        elif password_attempt.strip() == '':
            messagebox.showinfo(message='Password field empty')
        elif success == (True, True):
            homepage_window(customer)
        elif success == (True, False):
            messagebox.showinfo(message='Incorrect password')
            login_attempts += 1
        else:
            messagebox.showinfo(message='Not a valid username')

    for old_el in elements.values():
        old_el.grid_forget()  # clear screen
    elements.clear()  # clear dictionary
    opening_logo = ImageTk.PhotoImage(img_logo)
    comp_name_logo = tk.Label(master=root, image=opening_logo)
    comp_name_logo.image = opening_logo
    username_label = tk.Label(master=root, text='Username: ', fg='black', bg='white', font=('Courier', 14))
    username_entry = tk.Entry(master=root, bg='#F0F0F0')
    password_label = tk.Label(master=root, text='Password: ', fg='black', bg='white', font=('Courier', 14))
    password_entry = tk.Entry(master=root, bg='#F0F0F0')
    login_button = tk.Button(master=root, text='Login', font=('Courier', 14), command=login_request)
    new_button = tk.Button(master=root, text='New?', font=('Courier', 14), command=new_user_window)
    # grid elements for window 1
    comp_name_logo.grid(row=0, column=0, columnspan=2)
    username_label.grid(row=1, column=0, padx=5, pady=5)
    username_entry.grid(row=1, column=1, padx=15, pady=5, sticky='ew')
    password_label.grid(row=2, column=0, padx=5, pady=5)
    password_entry.grid(row=2, column=1, padx=15, pady=5, sticky='ew')
    login_button.grid(row=3, column=0, padx=5, pady=5)
    new_button.grid(row=3, column=1, padx=5, pady=5)
    elements['comp_logo'] = comp_name_logo
    elements['username label'] = username_label
    elements['username entry'] = username_entry
    elements['password label'] = password_label
    elements['password entry'] = password_entry
    elements['login button'] = login_button
    elements['new button'] = new_button


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Josepe Bank (not a real bank)')
    logo_icon = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/logo_icon.ico'))
    root.tk.call('wm', 'iconphoto', root._w, logo_icon)
    root.configure(bg='white')
    img_logo = Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/JosepeBankLogo.png')
    elements = {}
    login_page()
    root.mainloop()
