class DocManager:
    def __init__(self, account, statement_file: str, notice_file: str):
        self.account = account
        self.statement_file = statement_file
        self.notice_file = notice_file

    def withdraw_lim_notice(self, timestamp, past_limit=True):
        with open(self.notice_file, 'a') as f:
            if not past_limit:
                f.write('{}\nDear {},\nYour withdrawal limit of {} has been reached. Future withdrawals for this '
                        'month will not be approved.\n{}\n'.format(timestamp.strftime('%B %d, %Y'),
                                                                   self.account.owners[0].name.split()[0],
                                                                   self.account.withdrawal_lim, '-' * 100))
            else:
                f.write('{}\nDear {},\nYour withdrawal limit of {} has been reached. Today\'s withdrawal was not '
                        'approved.\n{}\n'.format(timestamp.strftime('%B %d, %Y'),
                                                 self.account.owners[0].name.split()[0], self.account.withdrawal_lim,
                                                 '-' * 100))

    def overdraft_notice(self, timestamp):
        with open(self.statement_file, 'a') as f:
            f.write('{}\n- ${:.2f} (OVERDRAFT FEE)\nBalance: ${:.2f}\n{}\n'.format(timestamp.strftime('%B %d, %Y'),
                                                                                   self.account.overdraft_fee,
                                                                                   self.account.balance, '-' * 100))
        with open(self.notice_file, 'a') as f:
            f.write('{}\nDear {},\nYour account has dropped beneath the minimum balance of ${:.2f}. An overdraft fee '
                    'of ${:.2f} has been \ncharged to your account.\n{}'
                    '\n'.format(timestamp.strftime('%B %d, %Y'), self.account.owners[0].name.split()[0],
                                self.account.minimum_bal, self.account.overdraft_fee, '-' * 100))

    def transaction_notice(self, trans_type: str, amount: float, timestamp):
        if trans_type == 'deposit':
            with open(self.statement_file, 'a') as f:
                f.write('{}\n+ ${:.2f}\nBalance: ${:.2f}\n{}\n'.format(timestamp.strftime('%B %d, %Y'), amount,
                                                                       self.account.balance, '-' * 100))
        elif trans_type in ('withdraw', 'withdrawal'):
            with open(self.statement_file, 'a') as f:
                f.write('{}\n- ${:.2f}\nBalance: ${:.2f}\n{}\n'.format(timestamp.strftime('%B %d, %Y'), amount,
                                                                       self.account.balance, '-' * 100))
        else:
            raise TypeError('Invalid parameter {}. Expected \'deposit\' or \'withdraw\''.format(trans_type))

    def change_notice(self, changed_item: str, item_value, timestamp):
        with open(self.notice_file, 'a') as f:
            f.write('{}\nDear {},\nYour {} has been changed to {}.\n{}\n'.format(timestamp.strftime('%B %d, %Y'),
                                                                                 self.account.owners[0].name.split()[0],
                                                                                 changed_item, item_value, '-' * 100))

    def add_customer_notice(self, customer, timestamp):
        with open(self.notice_file, 'a') as f:
            f.write('{}\nDear {},\n{} has successfully been added as an account owner.\n{}'
                    '\n'.format(timestamp.strftime('%B %d, %Y'), self.account.owners[0].name.split()[0], customer.name,
                                '-' * 100))

    def remove_customer_notice(self, customer, timestamp):
        with open(self.notice_file, 'a') as f:
            f.write('{}\nDear {},\n{} has successfully been removed from being an account owner.\n{}'
                    '\n'.format(timestamp.strftime('%B %d, %Y'), self.account.owners[0].name.split()[0], customer.name,
                                '-' * 100))

    def no_owner_notice(self, timestamp):
        with open(self.notice_file, 'a') as f:
            f.write('{}\nAll owners have been removed from the account.'.format(timestamp.strftime('%B %d, %Y')))
