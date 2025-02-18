class UsersException:
    registration_successful: str = "Реєстрація успішна"
    already_exist: str = "Користувач з вказаним логіном вже існує"
    not_exist: str = "Користувач відсутній"
    invalid_password: str = "Пароль має містити не менше 8 символів"
    invalid_username: str = "Логін користувача має містити від 3 до 50 символів"
    invalid_first_name: str = "Ім'я користувача має містити від 2 до 25 символів"
    bad_login: str = "Невірне ім'я користувача або пароль"
