from modules.money import Money
from modules.database import Database
import requests


def check_alert():
    money_dict, position = Money.search_data()
    all_user = []
    data = Database.find_all(collection="users")
    for user in data:
        all_user.append(user["email"])
    for user in all_user:
        message = []
        user_all_alert = Database.find(collection="all_alert", query={"email": user})
        for user_alert in user_all_alert:
            if user_alert["rate_exchange"] == "cash":
                if money_dict[position[user_alert["currency"]]].cash_in != "-":
                    if float(user_alert["price"][0]) >= float(money_dict[position[user_alert["currency"]]].cash_in):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    elif money_dict[position[user_alert["currency"]]].cash_out != "-":
                        if float(user_alert["price"][0]) <= float(
                                money_dict[position[user_alert["currency"]]].cash_out):
                            if user_alert["currency"] not in message:
                                message.append(user_alert["currency"])
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif money_dict[position[user_alert["currency"]]].cash_out != "-":
                    if float(user_alert["price"][0]) <= float(money_dict[position[user_alert["currency"]]].cash_out):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

            if user_alert["rate_exchange"] == "sign":
                if money_dict[position[user_alert["currency"]]].sign_in != "-":
                    if float(user_alert["price"][0]) >= float(money_dict[position[user_alert["currency"]]].sign_in):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    elif money_dict[position[user_alert["currency"]]].sign_out != "-":
                        if float(user_alert["price"][0]) <= float(
                                money_dict[position[user_alert["currency"]]].sign_out):
                            if user_alert["currency"] not in message:
                                message.append(user_alert["currency"])
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                elif money_dict[position[user_alert["currency"]]].sign_out != "-":
                    if float(user_alert["price"][0]) <= float(
                            money_dict[position[user_alert["currency"]]].sign_out):
                        if user_alert["currency"] not in message:
                            message.append(user_alert["currency"])
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

            else:
                pass
        print(user, " : ", message)
        requests.post(
            "https://api.mailgun.net/v3/sandbox1b96a1ed36554268902d683b941720e5.mailgun.org/messages",
            auth=("api", "d71c327fcef21d1ae76ab199208f2269-49a2671e-37cd89ca"),
            data={"from": "Mailgun Sandbox <postmaster@sandbox1b96a1ed36554268902d683b941720e5.mailgun.org>",
                  "to": user,
                  "subject": "汇率变动提醒",
                  "text": "目前符合的货币为：{},具体请查看提醒页面！".format(str(message).strip("[]"))})


# Database.initialize()
# check_alert()
