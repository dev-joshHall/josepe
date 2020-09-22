import tkinter as tk
from tkinter import ttk
import re
from PIL import ImageTk, Image
from tkinter import messagebox
from datetime import datetime
from googletrans import Translator
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


def translate(text):
    if settings['language'] != 'en':
        return tran.translate(text, dest=settings['language']).text
    return text


def update_language(_):
    if lang_val.get() == '':
        settings['language'] = 'en'
    else:
        settings['language'] = lang_symbols[lang_val.get()]


def update_theme(_):
    fg, bg = None, None
    if theme_val.get() in ('', 'Standard Theme'):
        fg, bg = 'black', 'white'
    elif theme_val.get() == 'Dark Theme':
        fg, bg = 'white', '#333333'
    elif theme_val.get() == 'Red Theme':
        fg, bg = 'black', '#8E1600'
    label_style.configure('BW.TLabel', foreground=fg, background=bg)
    radio_style.configure('Wild.TRadiobutton', foreground=fg, background=bg)
    root.configure(bg=bg)


def handle_focus_in(entry, display):
    if entry.get() == display:
        entry.delete(0, tk.END)
    entry.config()


def handle_focus_out(entry, display):
    if len(entry.get()) == 0:
        entry.delete(0, tk.END)
        entry.config()
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
                        messagebox.showinfo(message=translate('${:.2f} has been deposited'.format(amount)))
                        amount_entry.delete(0, tk.END)
                    elif radio_val.get() == 'withdraw':
                        bank_account.withdraw(amount)
                        messagebox.showinfo(message=translate('${:.2f} has been withdrawn'.format(amount)))
                        amount_entry.delete(0, tk.END)
                    else:
                        messagebox.showinfo(message=translate('Select transaction type'))
                else:
                    messagebox.showinfo(message=translate('Enter an amount (US Dollars)'))

            clear_window(exclude=['img label', 'signout button', 'back button'])
            back_btn.config(command=lambda: select_option(bank_account))
            elements['img label'].grid(row=0, column=0, columnspan=3)
            elements['signout button'].grid(row=1, column=2, sticky='nes')
            radio_val.set(None)
            deposit_radio = ttk.Radiobutton(master=root, text=translate('Deposit'), variable=radio_val, value='deposit',
                                            style='Wild.TRadiobutton')
            withdraw_radio = ttk.Radiobutton(master=root, text=translate('Withdraw'), variable=radio_val,
                                             value='withdraw', style='Wild.TRadiobutton')
            amount_entry = ttk.Entry(master=root)
            process_button = ttk.Button(master=root, text=translate('Process Transaction'), command=process_command)
            deposit_radio.grid(row=2, column=1)
            withdraw_radio.grid(row=3, column=1)
            amount_entry.grid(row=4, column=1)
            process_button.grid(row=5, column=1, pady=5, padx=5)
            amount_entry.insert(0, translate('Amount'))
            amount_entry.bind("<FocusIn>", lambda x: handle_focus_in(amount_entry, translate('Amount')))
            amount_entry.bind("<FocusOut>", lambda x: handle_focus_out(amount_entry, translate('Amount')))
            elements['deposit radio'] = deposit_radio
            elements['withdraw radio'] = withdraw_radio
            elements['amount entry'] = amount_entry
            elements['process button'] = process_button

        def manage_owners():
            def remove_owner(account_owner):
                bank_account.remove_customer(account_owner)
                manage_owners()

            def add_owner_window():
                def add_owner():
                    username = owner_username_entry.get()
                    owner_username_entry.delete(0, tk.END)
                    if username:
                        for customer in admin.customers:
                            if customer.email == username:
                                if customer not in bank_account.owners:
                                    bank_account.add_customer(customer)
                                    messagebox.showinfo(
                                        message=translate('{} successfully added to account'.format(customer.name)))
                                else:
                                    messagebox.showinfo(
                                        message=translate('{} is already an account owner'.format(customer.name)))
                                break
                        else:
                            messagebox.showinfo(message=translate('Customer \'{}\' not found'.format(username)))
                    else:
                        messagebox.showinfo(
                            message=translate('Enter the username for a customer\nto add to the account'))
                clear_window(exclude=['img label', 'signout button', 'back button'])
                back_btn.config(command=manage_owners)
                owner_username_lbl = ttk.Label(master=root, text=translate('Username:'), style='BW.TLabel')
                owner_username_entry = ttk.Entry(master=root)
                add_owner_btn = ttk.Button(master=root, text=translate('Add Owner'), command=add_owner)
                owner_username_lbl.grid(row=3, column=0)
                owner_username_entry.grid(row=3, column=1)
                add_owner_btn.grid(row=4, column=0, columnspan=2)
                elements['owner username lbl'] = owner_username_lbl
                elements['owner username entry'] = owner_username_entry
                elements['add owner btn'] = add_owner_btn
            clear_window(exclude=['img label', 'signout button', 'back button'])
            back_btn.config(command=lambda: select_option(bank_account))
            if bank_account.owners:
                label_text = 'Owners for account ***-****-{}:'.format(bank_account.account_number[-4:])
            else:
                label_text = 'There are no owners for account ***-****-{}:'.format(bank_account.account_number[-4:])
            owners_label = ttk.Label(master=root, text=translate(label_text), style='BW.TLabel')
            row_to_grid = 3
            owners_label.grid(row=2, column=0, columnspan=2, sticky='nesw')
            elements['owners label'] = owners_label
            for owner in bank_account.owners:
                lbl = ttk.Label(master=root, text=owner.name if owner else 'None', style='BW.TLabel')
                lbl.grid(row=row_to_grid, column=0)
                btn = ttk.Button(master=root, text=translate('Remove Owner'), command=lambda: remove_owner(owner))
                btn.grid(row=row_to_grid, column=1)
                row_to_grid += 1
                elements['owner label {}'.format(row_to_grid - 3)] = lbl
                elements['owner remove button {}'.format(row_to_grid - 3)] = btn
            add_owner_button = ttk.Button(master=root, text=translate('Add Owner'), command=add_owner_window)
            add_owner_button.grid(row=row_to_grid, column=0, columnspan=2)
            elements['add owner button'] = add_owner_button

        clear_window(exclude=['img label', 'signout button', 'back button'])
        elements['img label'].grid(row=0, column=0, columnspan=2)
        elements['signout button'].grid(row=1, column=1, sticky='nes')
        back_btn.config(command=lambda: accounts_window(user))
        trans_option_button = ttk.Button(master=root, text=translate('Deposit or Withdraw Money'),
                                         command=transaction_win)
        manage_owners_button = ttk.Button(master=root, text=translate('Add or Remove Account Owners'),
                                          command=manage_owners)
        trans_option_button.grid(row=2, column=0, columnspan=2, sticky='nesw', ipady=10)
        manage_owners_button.grid(row=3, column=0, columnspan=2, sticky='nesw', ipady=10)
        elements['transaction option button'] = trans_option_button
        elements['manage owners button'] = manage_owners_button

    def new_account_win():
        def create_account():
            amount = start_dep_entry.get()
            if amount.replace('.', '', 1).isnumeric():
                amount = float(amount)
                if radio_val2.get() == 'savings':
                    new_account = SavingsAccount(owners=[user], balance=amount, administration=admin)
                    messagebox.showinfo(message=translate('Your account {}\nhas been '
                                                          'created'.format(new_account.account_number)))
                    start_dep_entry.delete(0, tk.END)
                elif radio_val2.get() == 'checking':
                    new_account = CheckingAccount(owners=[user], balance=amount, administration=admin)
                    messagebox.showinfo(message=translate('Your account {}\nhas been '
                                                          'created'.format(new_account.account_number)))
                    start_dep_entry.delete(0, tk.END)
                else:
                    messagebox.showinfo(message=translate('Select account type'))
            else:
                messagebox.showinfo(message=translate('Enter an amount (US Dollars)'))

        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: accounts_window(user))
        acc_type_label = ttk.Label(master=root, text=translate('Account type:'), style='BW.TLabel')
        start_dep_label = ttk.Label(master=root, text=translate('Initial deposit:'), style='BW.TLabel')
        start_dep_entry = ttk.Entry(master=root)
        create_acc_button = ttk.Button(master=root, text=translate('Create Account'), command=create_account)
        radio_val2.set(None)
        savings_radio = ttk.Radiobutton(master=root, text=translate('Savings'), variable=radio_val2, value='savings',
                                        style='Wild.TRadiobutton')
        checking_radio = ttk.Radiobutton(master=root, text=translate('Checking'), variable=radio_val2, value='checking',
                                         style='Wild.TRadiobutton')
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
    back_btn = ttk.Button(master=root, text=translate('Back'), command=lambda: homepage_window(user))
    back_btn.grid(row=1, column=0, sticky='nsw')
    row = 2
    for account in user.bank_accounts:
        button = ttk.Button(text=translate('Account: ***-****-{}\t\t'
                                           'Balance: ${:.2f}'.format(account.account_number[-4:], account.balance)),
                            command=lambda: select_option(account))
        button.grid(row=row, column=0, columnspan=2, sticky='nesw', ipady=10)
        elements['account button {}'.format(row - 1)] = button
        row += 1
    new_account_button = ttk.Button(master=root, text=translate('Start an Account'), command=lambda: new_account_win())
    new_account_button.grid(row=row, column=0, columnspan=2, sticky='nesw', ipady=10)
    elements['back button'] = back_btn
    elements['new_account'] = new_account_button


def documents_window(user):
    def statement_window():
        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: documents_window(user))
        with open('BankStatement.txt', 'r') as f:
            statement = f.read()
            text = 'Statement:\n\n{}'.format(statement)
            statement_combobox = ttk.Combobox(master=root, text=translate(text))
            statement_combobox.grid(row=2, column=0, columnspan=2, sticky='nesw')
            elements['statement combobox'] = statement_combobox

    def notices_window():
        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: documents_window(user))
        with open('BankNotices.txt', 'r') as f:
            notices = f.read()
            notices_label = ttk.Label(master=root, text=translate('Notices:\n\n{}'.format(notices)), style='BW.TLabel')
            notices_label.grid(row=2, column=0, columnspan=2, sticky='nesw')
            elements['notices label'] = notices_label

    clear_window(exclude=['img label', 'signout button'])
    root.title('Josepe Bank (not a real bank) - {}\'s Documents'.format(user.name.split()[0]))
    back_btn = ttk.Button(master=root, text=translate('Back'), command=lambda: homepage_window(user))
    statement_button = ttk.Button(master=root, text=translate('Statement'), command=statement_window)
    notices_button = ttk.Button(master=root, text=translate('Notices'), command=notices_window)
    back_btn.grid(row=1, column=0, sticky='nsw')
    statement_button.grid(row=2, column=0, columnspan=2, sticky='nesw', ipady=10)
    notices_button.grid(row=3, column=0, columnspan=2, sticky='nesw', ipady=10)
    elements['back button'] = back_btn
    elements['statement button'] = statement_button
    elements['notices button'] = notices_button


def settings_window(user):
    def account_settings():
        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: settings_window(user))
        select_theme_lbl = ttk.Label(master=root, text=translate('Select Theme:'), style='BW.TLabel')
        theme_chosen = ttk.Combobox(master=root, textvariable=theme_val)
        theme_chosen.bind('<<ComboboxSelected>>', update_theme)
        theme_chosen['values'] = ('Standard Theme', 'Dark Theme', 'Red Theme')
        select_theme_lbl.grid(row=2, column=0)
        theme_chosen.grid(row=2, column=1)
        elements['blank label'].grid(row=3, column=0, columnspan=2)
        theme_chosen.current()
        elements['select theme label'] = select_theme_lbl
        elements['theme combobox'] = theme_chosen

    def language_settings():
        clear_window(exclude=['img label', 'signout button', 'back button'])
        back_btn.config(command=lambda: settings_window(user))
        select_lang_lbl = ttk.Label(master=root, text=translate('Select Language:'), style='BW.TLabel')
        language_chosen = ttk.Combobox(master=root, textvariable=lang_val)
        language_chosen.bind('<<ComboboxSelected>>', update_language)
        language_chosen['values'] = (
            'Arabic',
            'Armenian',
            'Bulgarian',
            'Czech',
            'Chinese',
            'Danish',
            'Dutch',
            'English',
            'Estonian',
            'Finnish',
            'French',
            'German',
            'Greek',
            'Hebrew',
            'Hindi',
            'Hungarian',
            'Indonesian',
            'Italian',
            'Japanese',
            'Korean',
            'Latin',
            'Macedonian',
            'Nepali',
            'Norwegian',
            'Polish',
            'Portuguese',
            'Romanian',
            'Russian',
            'Slovak',
            'Slovenian',
            'Somali',
            'Spanish',
            'Swedish',
            'Swahili',
            'Thai',
            'Turkish',
            'Ukrainian',
            'Vietnamese',
            'Welsh',
            'Zulu'
        )
        select_lang_lbl.grid(row=2, column=0)
        language_chosen.grid(row=2, column=1)
        elements['blank label'].grid(row=3, column=0, columnspan=2)
        language_chosen.current()
        elements['select language label'] = select_lang_lbl
        elements['language combobox'] = language_chosen

    clear_window(exclude=['img label', 'signout button'])
    root.title('Josepe Bank (not a real bank) - {}\'s Settings'.format(user.name.split()[0]))
    elements['signout button'].config(text=translate('Sign out'))
    back_btn = ttk.Button(master=root, text=translate('Back'), command=lambda: homepage_window(user))

    account_settings_btn = ttk.Button(master=root, text=translate('My Account'), command=account_settings)
    language_settings_btn = ttk.Button(master=root, text=translate('Language'), command=language_settings)
    back_btn.grid(row=1, column=0, sticky='nsw')
    account_settings_btn.grid(row=2, column=0, columnspan=2, sticky='nesw', ipady=10)
    language_settings_btn.grid(row=3, column=0, columnspan=2, sticky='nesw', ipady=10)
    elements['back button'] = back_btn
    elements['account settings button'] = account_settings_btn
    elements['language settings button'] = language_settings_btn


def homepage_window(user):
    def sign_out():
        documents_button.image, accounts_button.image, settings_button.image, img_label.image = None, None, None, None
        login_page()

    root.title('Josepe Bank (not a real bank) - {}\'s profile'.format(user.name.split()[0]))
    clear_window()
    img_1 = ImageTk.PhotoImage(Image.open('stack-of-manuals.png'))
    img_2 = ImageTk.PhotoImage(Image.open('accounts.jpg'))
    img_3 = ImageTk.PhotoImage(Image.open('settings.jpg'))
    img_4 = img_logo.resize((604, 180), Image.ANTIALIAS)
    img_4 = ImageTk.PhotoImage(img_4)
    img_label = ttk.Label(master=root, image=img_4, style='BW.TLabel')
    welcome_label = ttk.Label(master=root, text=translate('Welcome {}!'.format(user.name.split()[0])), anchor='w',
                              style='BW.TLabel')
    signout_button = ttk.Button(master=root, text=translate('Sign out'), command=sign_out)
    accounts_button = ttk.Button(master=root, image=img_2, command=lambda: accounts_window(user))
    documents_button = ttk.Button(master=root, image=img_1, command=lambda: documents_window(user))
    settings_button = ttk.Button(master=root, image=img_3, command=lambda: settings_window(user))
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
            messagebox.showinfo(message=translate('Not a valid email address'))
            return -1
        # verify password
        if password == confirmed_pass:
            password_pattern = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
            password_matches = password_pattern.finditer(password)
            if not [i for i in password_matches]:
                messagebox.showinfo(message=translate('The password must contain:\n  - A number\n  - A lowercase '
                                                      'letter\n  - An uppercase letter'))
                return -1
        else:
            messagebox.showinfo(message=translate('Password and Confirmed Password should be the same'))
            return -1
        # verify date of birth
        date_pattern = re.compile(r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$')
        date_matches = date_pattern.finditer(date_of_birth)
        if not [i for i in date_matches]:
            messagebox.showinfo(message=translate('Enter a valid date of birth ') + '(DD/MM/YYYY)')
            return -1
        # verify phone
        phone_pattern = re.compile(r'^[2-9]\d{2}-?\d{3}-?\d{4}$')
        password_matches = phone_pattern.finditer(phone)
        if not [i for i in password_matches]:
            messagebox.showinfo(message=translate('Enter a valid phone number'))
            return -1
        if not address:
            messagebox.showinfo(message=translate('Enter an address'))
            return -1
        date_of_birth = datetime.strptime(date_of_birth, '%m/%d/%Y')
        user = Customer(name, date_of_birth, address, phone, email, password, admin)
        homepage_window(user=user)

    # clear old elements from screen
    clear_window(exclude=['comp_logo'])
    # create new elements
    email_label = ttk.Label(master=root, text=translate('Email address: '), style='BW.TLabel')
    email_entry = ttk.Entry(master=root)
    pass_label = ttk.Label(master=root, text=translate('Password: '), style='BW.TLabel')
    pass_entry = ttk.Entry(master=root)
    confirm_pass_label = ttk.Label(master=root, text=translate('Confirm password: '), style='BW.TLabel')
    confirm_pass_entry = ttk.Entry(master=root)
    create_profile_button = ttk.Button(text=translate('Create profile'), command=create_account)
    back_button = ttk.Button(master=root, text=translate('{}Back{}'.format(' ' * 25, ' ' * 25)), command=login_page)
    name_label = ttk.Label(master=root, text=translate('Full name: '), style='BW.TLabel')
    name_entry = ttk.Entry(master=root)
    DOB_label = ttk.Label(master=root, text=translate('Date of Birth: '), style='BW.TLabel')
    DOB_entry = ttk.Entry(master=root)
    phone_label = ttk.Label(master=root, text=translate('Phone number: '), style='BW.TLabel')
    phone_entry = ttk.Entry(master=root)
    address_label = ttk.Label(master=root, text=translate('Address: '), style='BW.TLabel')
    address_entry = ttk.Entry(master=root)
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
            messagebox.showinfo(message=translate('Too many login attempts'))
        elif username_attempt.strip() == '':
            messagebox.showinfo(message=translate('Username field empty'))
        elif password_attempt.strip() == '':
            messagebox.showinfo(message=translate('Password field empty'))
        elif success == (True, True):
            homepage_window(customer)
        elif success == (True, False):
            messagebox.showinfo(message=translate('Incorrect password'))
            login_attempts += 1
        else:
            messagebox.showinfo(message=translate('Not a valid username'))

    for old_el in elements.values():
        old_el.grid_forget()  # clear screen
    elements.clear()  # clear dictionary
    opening_logo = ImageTk.PhotoImage(img_logo)
    comp_name_logo = ttk.Label(master=root, image=opening_logo, style='BW.TLabel')
    comp_name_logo.image = opening_logo
    username_label = ttk.Label(master=root, text=translate('Username: '), style='BW.TLabel')
    username_entry = ttk.Entry(master=root)
    password_label = ttk.Label(master=root, text=translate('Password: '), style='BW.TLabel')
    password_entry = ttk.Entry(master=root)
    login_button = ttk.Button(master=root, text=translate('Login'), command=login_request)
    new_button = ttk.Button(master=root, text=translate('New?'), command=new_user_window)
    blank_label = ttk.Label(master=root, text=' ', style='BW.TLabel')
    # grid elements for window 1
    comp_name_logo.grid(row=0, column=0, columnspan=2)
    username_label.grid(row=1, column=0, pady=5)
    username_entry.grid(row=1, column=1, padx=15, pady=5, sticky='ew')
    password_label.grid(row=2, column=0, pady=5)
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
    elements['blank label'] = blank_label


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Josepe Bank (not a real bank)')
    logo_icon = ImageTk.PhotoImage(Image.open('logo_icon.ico'))
    root.tk.call('wm', 'iconphoto', root._w, logo_icon)
    root.configure(bg='white')
    img_logo = Image.open('JosepeBankLogo.png')
    tran = Translator()
    elements = {}
    settings = {'language': 'en'}
    radio_val = tk.StringVar()
    radio_val2 = tk.StringVar()
    lang_val = tk.StringVar()
    theme_val = tk.StringVar()
    lang_symbols = {
        'Arabic': 'ar',
        'Armenian': 'hy',
        'Bulgarian': 'bg',
        'Czech': 'cs',
        'Chinese': 'zh-cn',
        'Danish': 'da',
        'Dutch': 'nl',
        'English': 'en',
        'Estonian': 'et',
        'Finnish': 'fi',
        'French': 'fr',
        'German': 'de',
        'Greek': 'el',
        'Hebrew': 'iw',
        'Hindi': 'hi',
        'Hungarian': 'hu',
        'Indonesian': 'id',
        'Italian': 'it',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Latin': 'la',
        'Macedonian': 'mk',
        'Nepali': 'ne',
        'Norwegian': 'no',
        'Polish': 'pl',
        'Portuguese': 'pt',
        'Romanian': 'ro',
        'Russian': 'ru',
        'Slovak': 'sk',
        'Slovenian': 'sl',
        'Somali': 'so',
        'Spanish': 'es',
        'Swedish': 'sv',
        'Swahili': 'sw',
        'Thai': 'th',
        'Turkish': 'tr',
        'Ukrainian': 'uk',
        'Vietnamese': 'vi',
        'Welsh': 'cy',
        'Zulu': 'zu'
    }
    login_page()
    label_style = ttk.Style()
    label_style.configure('BW.TLabel', foreground='black', background='white')
    radio_style = ttk.Style()
    radio_style.configure('Wild.TRadiobutton', foreground='black', background='white')
    root.mainloop()
