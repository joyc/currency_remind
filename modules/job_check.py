from modules.money import Money
from modules.database import Database


def check_alert():
    money_dict, position = Money.search_data()
    all_user = []
    data = Database.find_all(collection="users")
    for user in data:
        all_user.append(user["email"])
