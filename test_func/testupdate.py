from modules.database import Database
from modules.user import User

Database.initialize()
Database.insert_one("users", {"name": "test1", "email":"test1@test.com"})
User.update_user_email("test1@test.com", "test@test.net")
