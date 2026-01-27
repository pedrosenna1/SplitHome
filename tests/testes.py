from tests.login import correct_login, email_incorrect, password_incorrect
from tests.cadastro import correct_cadastro


def tests():
    correct_login()
    email_incorrect()
    password_incorrect()
    correct_cadastro()

if __name__ == "__main__":
    tests()