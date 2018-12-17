from modules.database import Database
from passlib.hash import pbkdf2_sha512


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save_to_db(self):
        Database.insert_many(collection="users", data=self.json())

    def json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def hash_password(self, password):
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_password(self, password, hash_password):
        return pbkdf2_sha512.verify(password, hash_password)
