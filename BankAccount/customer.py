class Customer:
    def __init__(self, name: str, date_of_birth, address: str, phone: str, email: str, password: str, admin):
        self.name = name
        self.date_of_birth = date_of_birth
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.admin = admin
        self.admin.customers.append(self)
        self.bank_accounts = []

    def __repr__(self):
        return 'Customer: {}'.format(self.name)

