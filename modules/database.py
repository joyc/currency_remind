import pymongo

# for test
# client = pymongo.MongoClient(['localhost:27017'])
# DATABASE = client['class']
# DATABASE['student'].insert_one({"name": "hython", "sex": "male", "age": "28", "tall": "175cm"})
# print(DATABASE['student'].find_one({"name": "hython"}))


class Database:
    URI = ["localhost:27017"]
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['currency']

    @staticmethod
    def insert_one(collection, data):
        return Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def insert_many(collection, data):
        return Database.DATABASE[collection].insert_many(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def find_all(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def update(collection, query, data):
        return Database.DATABASE[collection].update(query, data)

    @staticmethod
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)