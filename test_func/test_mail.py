import requests


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/sandbox1b96a1ed36554268902d683b941720e5.mailgun.org/messages",
        auth=("api", "d71c327fcef21d1ae76ab199208f2269-49a2671e-37cd89ca"),
        data={"from": "Mailgun Sandbox <postmaster@sandbox1b96a1ed36554268902d683b941720e5.mailgun.org>",
              "to": "Charlie Lee <rockbee@gmail.com>",
              "subject": "Hello Charlie Lee, 邮件提醒测试",
              "text": "Congratulations Charlie Lee, you just sent an email with Mailgun!  You are truly awesome!"
                      "这个是测试邮件！"})


send_simple_message()