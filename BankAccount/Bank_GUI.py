import tkinter as tk
import re
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import datetime
from bank_account import *
from admin import admin

login_attempts = 0
maggy = Customer('Maggy', 39, '1020 N 550 S Heber, UT', '9807593056', 'maggysmith@gmail.com', 'blabla', admin)
acc_1 = SavingsAccount(owners=[maggy], balance=300, administration=admin)


def clear_window(exclude: list = None):
    """
    Clears all items of a window except elements that are excluded.
    :param exclude: list of elements to exclude from being cleared
    :return: None
    """
    if exclude is None:
        exclude = []
    for key, old_el in elements.items():
        if key not in exclude and old_el:
            old_el.grid_forget()


def handle_focus_in(entry, display):
    if entry.get() == display:
        entry.delete(0, tk.END)
    entry.config(fg='black')


def handle_focus_out(entry, display):
    if len(entry.get()) == 0:
        entry.delete(0, tk.END)
        entry.config(fg='grey')
        entry.insert(0, display)


def accounts_window(user):
    def select_option(bank_account):
        def transaction_win():
            def process_command():
                amount = amount_entry.get()
                if amount.replace('.', '', 1).isnumeric():
                    amount = float(amount)
                    if radio_val.get() == 'deposit':
                        bank_account.deposit(amount)
                        messagebox.showinfo(message='${:.2f} has been deposited'.format(amount))
                        amount_entry.delete(0, tk.END)
                    elif radio_val.get() == 'withdraw':
                        bank_account.withdraw(amount)
                        messagebox.showinfo(message='${:.2f} has been withdrawn'.format(amount))
                        amount_entry.delete(0, tk.END)
                    else:
                        messagebox.showinfo(message='Select transaction type')
                else:
                    messagebox.showinfo(message='Enter an amount (US Dollars)')

            clear_window(exclude=['img label', 'signout button', 'back button'])
            back_btn.config(command=lambda: select_option(bank_account))
            elements['img label'].grid(row=0, column=0, columnspan=3)
            elements['signout button'].grid(row=1, column=2, sticky='nes')
            radio_val.set(None)
            deposit_radio = tk.Radiobutton(master=root, text='Deposit', variable=radio_val, value='deposit', bg='white',
                                           pady=5)
            withdraw_radio = tk.Radiobutton(master=root, text='Withdraw', variable=radio_val, value='withdraw',
                                            bg='white', pady=5)
            amount_entry = tk.Entry(master=root, bg='#F0F0F0', fg='grey')
            process_button = tk.Button(master=root, text='Process Transaction', padx=5, pady=5, command=process_command)
            deposit_radio.grid(row=2, column=1)
            withdraw_radio.grid(row=3, column=1)
            amount_entry.grid(row=4, column=1)
            process_button.grid(row=5, column=1, pady=5, padx=5)
            amount_entry.insert(0, 'Amount')
            amount_entry.bind("<FocusIn>", lambda x: handle_focus_in(amount_entry, 'Amount'))
            amount_entry.bind("<FocusOut>", lambda x: handle_focus_out(amount_entry, 'Amount'))
            elements['deposit radio'] = deposit_radio
            elements['withdraw radio'] = withdraw_radio
            elements['amount entry'] = amount_entry
            elements['process button'] = process_button

        def manage_owners():
            def remove_owner(account_owner):
                bank_account.remove_customer(account_owner)
                manage_owners()
            clear_window(exclude=['img label', 'signout button', 'back button'])
            back_btn.config(command=lambda: select_option(bank_account))
            if bank_account.owners:
                label_text = 'Owners for account ***-****-{}:'.format(bank_account.account_number[-4:])
            else:
                label_text = 'There are no owners for account ***-****-{}:'.format(bank_account.account_number[-4:])
            owners_label = tk.Label(master=root, pady=5, bg='white', text=label_text)
            row_to_grid = 2
            owners_label.grid(row=row_to_grid, column=0, columnspan=2, sticky='nesw')
            elements['owners label'] = owners_label
            for owner in bank_account.owners:
                row_to_grid += 1
                lbl = tk.Label(master=root, text=owner.name if owner else 'None', pady=5, bg='white')
                lbl.grid(row=row_to_grid, column=0)
                btn = tk.Button(master=root, text='Remove Owner', command=lambda: remove_owner(owner), pady=5, padx=5)
                btn.grid(row=row_to_grid, column=1, sticky='nsw')
                elements['owner label {}'.format(row_to_grid - 2)] = lbl
                elements['owner remove button {}'.format(row_to_grid - 2)] = btn

        clear_window(exclude=['img label', 'signout button', 'back button'])
        elements['img label'].grid(row=0, column=0, columnspan=2)
        elements['signout button'].grid(row=1, column=1, sticky='nes')
        back_btn.config(command=lambda: accounts_window(user))
        trans_option_button = tk.Button(master=root, text='Deposit or Withdraw Money', command=transaction_win, pady=10)
        manage_owners_button = tk.Button(master=root, text='Add or Remove Account Owners', command=manage_owners,
                                         pady=10)
        trans_option_button.grid(row=2, column=0, columnspan=2, sticky='nesw')
        manage_owners_button.grid(row=3, column=0, columnspan=2, sticky='nesw')
        elements['transaction option button'] = trans_option_button
        elements['manage owners button'] = manage_owners_button

    def new_account_win():
        def create_account():
            amount = start_dep_entry.get()
            if amount.replace('.', '', 1).isnumeric():
                amount = float(amount)
                if radio_val2.get() == 'savings':
                    new_account = SavingsAccount(owners=[user], balance=amount, administration=admin)
                    messagebox.showinfo(message='Your account {}\nhas been created'.format(new_account.account_number))
                    start_dep_entry.delete(0, tk.END)
                elif radio_val2.get() == 'checking':
                    new_account = CheckingAccount(owners=[user], balance=amount, administration=admin)
                    messagebox.showinfo(message='Your account {}\nhas been created'.format(new_account.account_number))
                    start_dep_entry.delete(0, tk.END)
                else:
                    messagebox.showinfo(message='Select account type')
            else:
                messagebox.showinfo(message='Enter an amount (US Dollars)')

        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: accounts_window(user))
        acc_type_label = tk.Label(master=root, text='Account type:', pady=5, bg='white')
        start_dep_label = tk.Label(master=root, text='Initial deposit:', pady=5, bg='white')
        start_dep_entry = tk.Entry(master=root, bg='#F0F0F0')
        create_acc_button = tk.Button(master=root, text='Create Account', command=create_account, pady=5, padx=10)
        radio_val2.set(None)
        savings_radio = tk.Radiobutton(master=root, text='Savings', variable=radio_val2, value='savings', bg='white')
        checking_radio = tk.Radiobutton(master=root, text='Checking', variable=radio_val2, value='checking', bg='white')
        acc_type_label.grid(row=2, column=0)
        savings_radio.grid(row=2, column=1)
        checking_radio.grid(row=3, column=1)
        start_dep_label.grid(row=4, column=0)
        start_dep_entry.grid(row=4, column=1)
        create_acc_button.grid(row=5, column=1)
        elements['account type label'] = acc_type_label
        elements['savings radio'] = savings_radio
        elements['checking radio'] = checking_radio
        elements['starting deposit label'] = start_dep_label
        elements['starting deposit entry'] = start_dep_entry
        elements['create account button'] = create_acc_button

    clear_window(exclude=['img label', 'signout button'])
    elements['img label'].grid(row=0, column=0, columnspan=2)
    elements['signout button'].grid(row=1, column=1, sticky='nes')
    root.title('Josepe Bank (not a real bank) - {}\'s Accounts'.format(user.name.split()[0]))
    back_btn = tk.Button(master=root, text='Back', command=lambda: homepage_window(user))
    back_btn.grid(row=1, column=0, sticky='nsw')
    row = 2
    for account in user.bank_accounts:
        button = tk.Button(text='Account: ***-****-{}\t\tBalance: ${:.2f}'.format(account.account_number[-4:],
                                                                                  account.balance), pady=10,
                           command=lambda: select_option(account))
        button.grid(row=row, column=0, columnspan=2, sticky='nesw')
        elements['account button {}'.format(row - 1)] = button
        row += 1
    new_account_button = tk.Button(master=root, text='Start an Account', command=lambda: new_account_win(), pady=10)
    new_account_button.grid(row=row, column=0, columnspan=2, sticky='nesw')
    elements['back button'] = back_btn
    elements['new_account'] = new_account_button


def documents_window(user):
    def statement_window():
        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: documents_window(user))
        with open('BankStatement.txt', 'r') as f:
            statement = f.read()
            statement_label = tk.Label(master=root, text='Statement:\n\n{}'.format(statement), bg='white')
            statement_label.grid(row=2, column=0, columnspan=2, sticky='nesw')
            elements['statement label'] = statement_label

    def notices_window():
        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: documents_window(user))
        with open('BankNotices.txt', 'r') as f:
            notices = f.read()
            notices_label = tk.Label(master=root, text='Notices:\n\n{}'.format(notices), bg='white')
            notices_label.grid(row=2, column=0, columnspan=2, sticky='nesw')
            elements['notices label'] = notices_label

    clear_window(exclude=['img label', 'signout button'])
    root.title('Josepe Bank (not a real bank) - {}\'s Documents'.format(user.name.split()[0]))
    back_btn = tk.Button(master=root, text='Back', command=lambda: homepage_window(user))
    statement_button = tk.Button(master=root, text='Statement', pady=10, command=statement_window)
    notices_button = tk.Button(master=root, text='Notices', pady=10, command=notices_window)
    back_btn.grid(row=1, column=0, sticky='nsw')
    statement_button.grid(row=2, column=0, columnspan=2, sticky='nesw')
    notices_button.grid(row=3, column=0, columnspan=2, sticky='nesw')
    elements['back button'] = back_btn
    elements['statement button'] = statement_button
    elements['notices button'] = notices_button


def settings_window(user):
    clear_window(exclude=['img label', 'signout button'])
    root.title('Josepe Bank (not a real bank) - {}\'s Settings'.format(user.name.split()[0]))
    back_btn = tk.Button(master=root, text='Back', command=lambda: homepage_window(user))
    back_btn.grid(row=1, column=0, sticky='nsw')
    elements['back button'] = back_btn


def homepage_window(user):
    def sign_out():
        documents_button.image, accounts_button.image, settings_button.image, img_label.image = None, None, None, None
        login_page()

    root.title('Josepe Bank (not a real bank) - {}\'s profile'.format(user.name.split()[0]))
    clear_window()
    img_1 = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/stack-of-manuals.png'))
    img_2 = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/accounts.jpg'))
    img_3 = ImageTk.PhotoImage(Image.open('C:/Users/jchca/OneDrive/Pictures/Saved Pictures/settings.jpg'))
    img_4 = img_logo.resize((604, 180), Image.ANTIALIAS)
    img_4 = ImageTk.PhotoImage(img_4)
    img_label = tk.Label(master=root, image=img_4, padx=0)
    welcome_label = tk.Label(master=root, text='Welcome {}!'.format(user.name.split()[0]), bg='white', padx=5, pady=10,
                             anchor='w')
    signout_button = tk.Button(master=root, text='Sign out', command=sign_out)
    accounts_button = tk.Button(master=root, image=img_2, command=lambda: accounts_window(user))
    documents_button = tk.Button(master=root, image=img_1, command=lambda: documents_window(user))
    settings_button = tk.Button(master=root, image=img_3, command=lambda: settings_window(user))
    documents_button.image, accounts_button.image, settings_button.image, img_label.image = img_1, img_2, img_3, img_4
    # grid elements
    img_label.grid(row=0, column=0, columnspan=2, sticky='nesw')
    welcome_label.grid(row=1, column=0, sticky='nesw')
    signout_button.grid(row=1, column=1, sticky='nes')
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

    # clear old elements from screen
    clear_window(exclude=['comp_logo'])
    # create new elements
    email_label = tk.Label(master=root, text='Email address: ', font=('Courier', 14), bg='white')
    email_entry = tk.Entry(master=root, bg='#F0F0F0')
    pass_label = tk.Label(master=root, text='Password: ', font=('Courier', 14), bg='white')
    pass_entry = tk.Entry(master=root, bg='#F0F0F0')
    confirm_pass_label = tk.Label(master=root, text='Confirm password: ', font=('Courier', 14), bg='white')
    confirm_pass_entry = tk.Entry(master=root, bg='#F0F0F0')
    create_profile_button = tk.Button(text='Create profile', command=create_account)
    back_button = tk.Button(master=root, text='{}Back{}'.format(' ' * 25, ' ' * 25), command=login_page)
    name_label = tk.Label(master=root, text='Full name: ', font=('Courier', 14), bg='white')
    name_entry = tk.Entry(master=root, bg='#F0F0F0')
    DOB_label = tk.Label(master=root, text='Date of Birth: ', font=('Courier', 14), bg='white')
    DOB_entry = tk.Entry(master=root, bg='#F0F0F0', fg='grey')
    phone_label = tk.Label(master=root, text='Phone number: ', font=('Courier', 14), bg='white')
    phone_entry = tk.Entry(master=root, bg='#F0F0F0', fg='grey')
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
    create_profile_button.grid(row=9, column=1, columnspan=2, padx=5, pady=5, sticky='ew')
    back_button.grid(row=9, column=0, padx=50, pady=5)
    DOB_entry.insert(0, 'MM/DD/YYYY')
    DOB_entry.bind("<FocusIn>", lambda x: handle_focus_in(DOB_entry, 'MM/DD/YYYY'))
    DOB_entry.bind("<FocusOut>", lambda x: handle_focus_out(DOB_entry, 'MM/DD/YYYY'))
    phone_entry.insert(0, 'XXX-XXX-XXXX')
    phone_entry.bind("<FocusIn>", lambda x: handle_focus_in(phone_entry, 'XXX-XXX-XXXX'))
    phone_entry.bind("<FocusOut>", lambda x: handle_focus_out(phone_entry, 'XXX-XXX-XXXX'))
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
    elements['back button'] = back_button


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
    login_button.grid(row=3, column=1, padx=5, pady=5)
    new_button.grid(row=3, column=0, padx=5, pady=5)
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
    radio_val = tk.StringVar()
    radio_val2 = tk.StringVar()
    login_page()
    root.mainloop()
