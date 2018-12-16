from modules.database import Database


Database.initialize()
Database.insert_one(collection="testdb", data={"name": "hython", "age": "28", "sex": "male"})
Database.insert_many(collection="testdb", data=[{"name": "hellen", "age": "32", "sex": "female"},
                                                {"name": "jesica", "age": "18", "sex": "female"}])
print(Database.find(collection="testdb", query={"sex": "female"})[0])
print(Database.find_one(collection="testdb", query={"name": "hython"}))
print(Database.find_all(collection="testdb")[1])
