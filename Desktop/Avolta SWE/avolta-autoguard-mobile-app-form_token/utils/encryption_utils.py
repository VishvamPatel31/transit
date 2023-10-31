import bcrypt


# Generate a random encryption key
def encrypt_password(password):
    encoded_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_pw, salt)

    # Returns a hashed password in the form of plain text
    return hashed_password.decode('utf-8')