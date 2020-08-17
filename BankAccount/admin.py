class Administration:
    def __init__(self):
        self.accounts = []
        self.admins = []
        self.customers = []

    def add_account(self, account):
        if hasattr(account, 'balance'):
            self.accounts.append(account)
        else:
            raise TypeError('{} is not an account'.format(account))

    def add_admin(self, administrator):
        if isinstance(administrator, Administrator):
            self.admins.append(administrator)
        else:
            raise TypeError('{} is not an administrator'.format(administrator))

    def change_overdraft_fee(self, new_fee, account):
        if account in self.accounts:
            if new_fee >= 0:
                account.overdraft_fee = new_fee
            else:
                raise ValueError('Fee must be >= 0')
        else:
            raise TypeError('Account \'{}\' not in Admin system'.format(account))

    def change_interest(self, new_interest: float, account):
        if account in self.accounts:
            account.interest = new_interest
        else:
            raise TypeError('Account \'{}\' not in Admin system'.format(account))

    def change_min_bal(self, new_min_bal: float, account):
        if account in self.accounts:
            if new_min_bal >= 0:
                account.minimum_bal = new_min_bal
            else:
                raise ValueError('Minimum balance level cannot be negative')
        else:
            raise TypeError('Account \'{}\' not in Admin system'.format(account))

    def change_withdraw_lim(self, new_limit: int, account):
        if account in self.accounts and hasattr(account, 'withdrawal_lim'):
            if new_limit >= 0:
                account.withdrawal_lim = new_limit
            else:
                raise ValueError('new_limit must be greater than or equal to 0')
        elif account in self.accounts:
            raise TypeError('Account \'{}\' is not a Savings Account'.format(account))
        else:
            raise TypeError('Account \'{}\' not in Admin system'.format(account))

    def approve_request(self, request_type: str):
        """
        :param request_type: Type of request from Customer.
        :return: bool
        """
        pass

    def new_month(self):
        """
        Send out statements. Clear old month's data from history and save it to a file.
        :return: None
        """
        pass

    def admin_login(self, username, password):
        booleans = [False, False]
        for administrator in self.admins:
            if username in (administrator.username, administrator.email):
                booleans[0] = True  # username or email is valid
                if password == administrator.password:
                    booleans[1] = True  # password is valid
                return tuple(booleans)
        else:
            return tuple(booleans)  # neither username or password are valid

    def customer_login(self, username, password):
        username = username.strip()
        password = password.strip()
        booleans = [False, False]
        for customer in self.customers:
            if username == customer.email:
                booleans[0] = True  # email is valid
                if password == customer.password:
                    booleans[1] = True  # password is valid
                return tuple(booleans), customer  # return success booleans and customer object
        else:
            return tuple(booleans), None  # neither username or password are valid

    def logout(self):
        pass


class Administrator:
    def __init__(self, username: str, email: str, password: str, phone: str, administration):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self.administration = administration
        self.administration.add_admin(self)  # add administrator to list of administrators in Administration

    def __repr__(self):
        return 'Admin: {}'.format(self.username)


admin = Administration()


if __name__ == '__main__':
    josh = Administrator('Josh Hall', 'jchcaleb@gmail.com', 'blabla', '3921924938', admin)
    # success = josh.administration.admin_login('Josh Hall', 'blabla')
    # print(admin.admins)
    # print(success)
