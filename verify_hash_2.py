import bcrypt

stored_hash = b"$2b$12$rl51IkMmvjs2rMO1lD8c6eXPg4VyGlaU2iOrrBRKqS2uiSh5NE.Hy"
password = b"Bienvewiva2024!!"

if bcrypt.checkpw(password, stored_hash):
    print("MATCH")
else:
    print("NO MATCH")
