from datetime import datetime as dt
from doc_manager import DocManager
from customer import Customer


class BankAccount:
    def __init__(self, owners: list, interest: float, balance: float, minimum_bal: float, overdraft_fee: float):
        if owners:
            self.owners = owners
        else:
            raise TypeError('Expected list of Customer object(s) in self.owners, but got empty list []')
        self.interest = interest
        self.balance = balance
        self.minimum_bal = minimum_bal
        self.overdraft_fee = overdraft_fee
        self.history = {'Deposits': [], 'Withdrawals': [], 'Fees': []}
        self.doc_manager = DocManager(self, 'BankStatement.txt', 'BankNotices.txt')

    def __repr__(self):
        return 'Account owner: {}.\nBalance: {}'.format(self.owners[0], self.balance)

    def add_customer(self, customer):
        if len(self.owners) < 2:
            self.owners.append(customer)
            self.doc_manager.add_customer_notice(customer, dt.today())
        else:
            raise TypeError('Maximum number of customers reached. Cannot add additional customers to account.')

    def remove_customer(self, customer):
        if customer in self.owners and len(self.owners) > 1:
            self.owners.remove(customer)
            self.doc_manager.remove_customer_notice(customer, dt.today())
        elif customer in self.owners and len(self.owners) == 1:
            self.owners.remove(customer)
            self.doc_manager.no_owner_notice(dt.today())
        else:
            raise TypeError('{} was not an owner of this account'.format(customer))

    def change_interest(self, new_interest: float):
        self.interest = new_interest

    def change_min_bal(self, new_min_bal: float):
        if new_min_bal >= 0:
            self.minimum_bal = new_min_bal
        else:
            raise ValueError('Minimum balance level cannot be negative')

    def charge_overdraft_fee(self):
        self.balance -= self.overdraft_fee
        self.doc_manager.overdraft_notice(dt.today())

    def change_overdraft_fee(self, new_fee):
        if new_fee >= 0:
            self.overdraft_fee = new_fee
        else:
            raise ValueError('Fee must be >= 0')

    def deposit(self, amount: float):
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
            # write transaction notice
            self.doc_manager.transaction_notice(trans_type='deposit', amount=amount, timestamp=timestamp)
        else:
            raise ValueError('Deposit amount must be positive')


class CheckingAccount(BankAccount):
    def withdraw(self, amount: float):
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
    def __init__(self, owners, interest, balance, minimum_bal, overdraft_fee, withdrawal_lim: int):
        super(SavingsAccount, self).__init__(owners, interest, balance, minimum_bal, overdraft_fee)
        self.withdrawal_lim = withdrawal_lim

    def change_withdraw_lim(self, new_limit: int):
        if new_limit >= 0:
            self.withdrawal_lim = new_limit
        else:
            raise ValueError('new_limit must be >= 0')

    def withdraw(self, amount: float):
        timestamp = dt.today()
        if len(self.history['Withdrawals']) < self.withdrawal_lim:
            if amount > 0:
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
            else:
                raise ValueError('Withdrawal amount must be positive')
        else:
            self.doc_manager.withdraw_lim_notice(timestamp, past_limit=True)


maggy = Customer('Maggy', 39, '1020 N 550 S Heber, UT', '9807593056', 'maggysmith@gmail.com', 480)
steve = Customer('Steve', 18, '1020 N 550 S Heber, UT', '9807593056', 'maggysmith@gmail.com', 220)
acc_1 = SavingsAccount(owners=[maggy], interest=.03, balance=300, minimum_bal=250, overdraft_fee=5, withdrawal_lim=2)
# print('History: {}\nBalance: {}'.format(acc_1.history, acc_1.balance))
# acc_1.deposit(300)
# acc_1.withdraw(150)
# acc_1.withdraw(5)
# acc_1.withdraw(447)
# print('History: {}\nBalance: {}'.format(acc_1.history, acc_1.balance))
print(acc_1.owners)
acc_1.add_customer(steve)
acc_1.remove_customer(maggy)
acc_1.remove_customer(steve)
print(acc_1.owners)
