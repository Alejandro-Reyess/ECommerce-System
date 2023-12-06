class Account():
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def login(self, username, password):
        return self.username == username and self.password == password

    def manage_profile(self, new_name, new_username, new_password):
        self.name = new_name
        self.username = new_username
        self.password = new_password


def create_account():
    name = input("Digite seu nome completo: ")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")
    return Account(name, username, password)

def login(account):
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")
    if account.login(username, password):
        print("Login verificado!")
    else:
        print("Nome de usuário ou senha incorretos!")

def manage_profile(account):
    new_name = input("Digite seu nome (deixe em branco para manter o atual): ")
    new_username = input("Digite seu novo nome de usuário (deixe em branco para manter o atual): ")
    new_password = input("Digite a nova senha (deixe em branco para manter a atual): ")

    if not new_name: new_name = account.name
    if not new_username: new_username = account.username
    if not new_password: new_password = account.password

    account.manage_profile(new_name, new_username, new_password)

