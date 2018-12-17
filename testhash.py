from passlib.hash import pbkdf2_sha512


password = input("Password")
hash_password = pbkdf2_sha512.hash(password)
print(hash_password)
print(pbkdf2_sha512.verify(password, hash_password))
