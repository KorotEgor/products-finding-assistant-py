def check_username(username):
    errs = []
    if not username:
        errs += ['Это обязательное поле']

    return errs


def check_email(email):
    errs = []
    if not email:
        errs += ['Это обязательное поле']
    elif "@" not in email:
        errs += ['В почте должен быть символ "@"']
    elif '.' not in email and '@.' not in email and email[-1] != '.':
        errs += ['В почте должен быть символ ".", но он не должен идти после "@" и быть последним']
    elif email.upper().isupper():
        errs += 'Почта должна содержать еще символы, кроме "@" и "."'

    return errs


def check_password(password):
    errs = []
    if not password:
        errs += ['Это обязательное поле']
    elif password.isdigit():
        errs += ["В пароле должны быть цифры"]
    elif len(password) < 8:
        errs += ["Длина пароля должна быть больше или равна 8"]
    elif password.isupper():
        errs += ["В пароле должны быть большие буквы"]
    elif password.islower():
        errs += ["В пароле должны быть маленькие буквы"]
    elif password.isalnum():
        errs += ["В пароле должны быть специальные символы"]

    return errs
