import bcrypt

password = b"Bienvewiva2024!!"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
print(hashed.decode('utf-8'))
