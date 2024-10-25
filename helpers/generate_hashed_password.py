from passlib.context import CryptContext

password_context = CryptContext(
    schemes=["bcrypt"],
)


def generate_password_hash(password: str) -> str:
    return password_context.hash(password)


password = "password"

print(generate_password_hash(password))
