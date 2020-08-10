class Customer:
    def __init__(self, name: str, age: int, address: str, phone: str, email: str, password: str):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.bank_accounts = []

    def __repr__(self):
        return 'Customer: {}'.format(self.name)

    def login(self):
        pass

    def logout(self):
        pass
