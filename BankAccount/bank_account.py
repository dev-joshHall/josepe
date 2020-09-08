from datetime import datetime as dt
from random import randint
from doc_manager import DocManager
from customer import Customer
from admin import Administration, Administrator, admin


class BankAccount:
    def __init__(self, owners: list, balance: float, administration):
        if owners:
            self.owners = owners
        else:
            raise TypeError('Expected list of Customer object(s) in self.owners, but got empty list []')
        for owner in self.owners:
            owner.bank_accounts.append(self)
        self.interest = None
        self.balance = balance
        self.minimum_bal = 30
        self.overdraft_fee = 5
        self.max_owner_qty = 2
        self.administration = administration
        self.administration.add_account(self)  # add this account to Administration's list of accounts
        # vv I need to change this! vv
        self.account_number = str(randint(10000000000, 99999999999))  # generates random number as account number
        self.history = {'Deposits': [], 'Withdrawals': [], 'Fees': []}
        self.doc_manager = DocManager(self, 'BankStatement.txt', 'BankNotices.txt')

    def __repr__(self):
        owner_names = [owner.name for owner in self.owners]
        return 'Account: {};\tOwner{}: {}'.format(self.account_number, 's' if len(self.owners) > 1 else '',
                                                  ', '.join([name.split()[0] for name in owner_names])
                                                  if self.owners else 'None')

    def add_customer(self, customer):
        """
        Adds a customer to associated object lists. Writes a notice to the user.
        :param customer: Customer object
        :return: None
        """
        if len(self.owners) < self.max_owner_qty:
            self.owners.append(customer)
            customer.bank_accounts.append(self)
            self.doc_manager.add_customer_notice(customer, dt.today())
        else:
            raise TypeError('Maximum number of customers reached. Cannot add additional customers to account.')

    def remove_customer(self, customer):
        """
        Removes a customer from associated object lists. Writes a notice to the user.
        :param customer: Customer object
        :return: None
        """
        if customer in self.owners and len(self.owners) > 1:
            self.owners.remove(customer)
            customer.bank_accounts.remove(self)
            self.doc_manager.remove_customer_notice(customer, dt.today())
        elif customer in self.owners and len(self.owners) == 1:
            customer.bank_accounts.remove(self)
            self.owners.remove(customer)
            self.doc_manager.no_owner_notice(dt.today())
        else:
            raise TypeError('{} was not an owner of this account'.format(customer))

    def charge_overdraft_fee(self):
        """
        Charges an overdraft fee to the account. Writes a notice to the user.
        :return: None
        """
        self.balance -= self.overdraft_fee
        self.doc_manager.overdraft_notice(dt.today())

    def deposit(self, amount: float):
        """
        Adds a given amount to the bank account. Add transaction to account's history. Notify the user of transaction.
        :param amount: float dollar amount
        :return: None
        """
        if amount > 0:
            self.balance += amount
            timestamp = dt.today()
            self.history['Deposits'].append(
                {
                    'Date': timestamp,
                    'Amount': amount,
                    'Balance': self.balance
                }
            )
            self.doc_manager.transaction_notice(trans_type='deposit', amount=amount, timestamp=timestamp)
        else:
            raise ValueError('Deposit amount must be positive')


class CheckingAccount(BankAccount):
    def __init__(self, owners, balance, administration):
        super(CheckingAccount, self).__init__(owners, balance, administration)
        self.interest = .1

    def withdraw(self, amount: float):
        """
        Removes an amount from the account's balance. Adds transaction to accounts history and notifies the user.
        :param amount: float amount of US Dollars
        :return: None
        """
        if amount > 0:
            self.balance -= amount
            timestamp = dt.today()
            self.history['Withdrawals'].append(
                {
                    'Date': timestamp,
                    'Amount': -amount,
                    'Balance': self.balance
                }
            )
            self.doc_manager.transaction_notice(trans_type='withdraw', amount=amount, timestamp=timestamp)
            if self.balance < self.minimum_bal:
                self.charge_overdraft_fee()
        else:
            raise ValueError('Withdrawal amount must be positive')


class SavingsAccount(BankAccount):
    def __init__(self, owners, balance, administration):
        super(SavingsAccount, self).__init__(owners, balance, administration)
        self.withdrawal_lim = 2
        self.interest = .3

    def withdraw(self, amount: float):
        """
        Removes an amount from the account's balance. Adds transaction to accounts history and notifies the user.
        Transaction is not approved if the number of withdrawals is at the withdrawal limit.
        :param amount: float amount of US Dollars
        :return: None
        """
        timestamp = dt.today()
        if len(self.history['Withdrawals']) < self.withdrawal_lim:
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.history['Withdrawals'].append(
                    {
                        'Date': timestamp,
                        'Amount': -amount,
                        'Balance': self.balance
                    }
                )
                self.doc_manager.transaction_notice(trans_type='withdraw', amount=amount, timestamp=timestamp)
                if len(self.history['Withdrawals']) == self.withdrawal_lim:
                    self.doc_manager.withdraw_lim_notice(timestamp, past_limit=False)
                if self.balance < self.minimum_bal:
                    self.charge_overdraft_fee()
            elif amount > 0:
                self.doc_manager.insufficient_balance_notice(timestamp, amount)
            else:
                raise ValueError('Withdrawal amount must be positive')
        else:
            self.doc_manager.withdraw_lim_notice(timestamp, past_limit=True)


if __name__ == '__main__':
    """Used to test the classes"""
    maggy = Customer('Maggy', 39, '1020 N 550 S Heber, UT', '9807593056', 'maggysmith@gmail.com', 'blabla', admin)
    steve = Customer('Steve', 18, '1020 N 550 S Heber, UT', '9807593056', 'maggysmith@gmail.com', 'password', admin)
    acc_1 = SavingsAccount(owners=[maggy], balance=300, administration=admin)
    # print('History: {}\nBalance: {}'.format(acc_1.history, acc_1.balance))
    acc_1.deposit(300)
    acc_1.withdraw(150)
    acc_1.withdraw(5)
    acc_1.withdraw(800)
    # print('History: {}\nBalance: {}'.format(acc_1.history, acc_1.balance))
    # print(acc_1.owners)
    # print(maggy.bank_accounts)
    acc_1.add_customer(steve)
    # acc_1.remove_customer(maggy)
    # acc_1.remove_customer(steve)
    # print(acc_1.owners)
    # print(maggy.bank_accounts, steve.bank_accounts)
    print(acc_1.withdrawal_lim)
    acc_1.administration.change_withdraw_lim(4, acc_1)
    print(acc_1.withdrawal_lim)
    print(acc_1)
