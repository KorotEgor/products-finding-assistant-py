def check_username(username):
    if not username:
        return ["Это обязательное поле"]

    return []


def check_email(email):
    errs = []
    if not email:
        return ["Это обязательное поле"]

    if "@" not in email:
        errs += ['В почте должен быть символ "@"']
    if "." not in email or "@." in email or email[-1] == ".":
        errs += [
            'В почте должен быть символ ".", но он не должен идти после "@" и быть последним',
        ]
    if not (email.upper().isupper() or email.isdigit()):
        errs += ['Почта должна содержать еще символы, кроме "@" и "."']

    return errs


def check_password(password):
    if not password:
        return ["Это обязательное поле"]

    errs = []
    if len(password) < 8:
        errs += ["Длина пароля должна быть больше или равна 8"]
    if not any(sym.isdigit() for sym in password):
        errs += ["В пароле должны быть цифры"]
    if not any(sym.isupper() for sym in password):
        errs += ["В пароле должны быть большие буквы"]
    if not any(sym.islower() for sym in password):
        errs += ["В пароле должны быть маленькие буквы"]
    if not any(sym.isalnum() for sym in password):
        errs += ["В пароле должны быть специальные символы"]

    return errs
