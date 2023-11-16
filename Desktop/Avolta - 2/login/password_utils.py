import bcrypt
from bcrypt import checkpw


# Generate a random encryption key
def hash_password(password):
    encoded_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_pw, salt)

    # Returns a hashed password in the form of plain text
    return hashed_password.decode('utf-8')

# check_password function
def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
