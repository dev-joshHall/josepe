class Customer:
    def __init__(self, name: str, age: int, address: str, phone: str, email: str, credit_score: int):
        self.name = name
        self.age = age
        self.address = address
        self.phone = phone
        self.email = email
        self.credit_score = credit_score

    def __repr__(self):
        return 'Customer object: {}'.format(self.name)
