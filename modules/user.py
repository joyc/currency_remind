from modules.database import Database
from passlib.hash import pbkdf2_sha512


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    @staticmethod
    def register_user(name, email, password):
        user_data = Database.find_one(collection="users", query={"email": email})
        if user_data is not None:
            return False
        User(name, email, User.hash_password(password)).save_to_db()
        return True

    @staticmethod
    def check_user(email, password):
        user_data = Database.find_one(collection="users", query={"email": email})
        if user_data is None:
            return False
        if User.check_password(password, user_data['password']) is False:
            return False
        return True

    def save_to_db(self):
        Database.insert_one(collection="users", data=self.json())

    def json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @staticmethod
    def hash_password(password):
        return pbkdf2_sha512.hash(password)

    @staticmethod
    def check_password(password, hash_password):
        return pbkdf2_sha512.verify(password, hash_password)

    @staticmethod
    def find_user_data(email):
        return Database.find_one(collection="users", query={"email": email})
