from flask import Flask, render_template, request, session, redirect
from modules.money import Money
from modules.user import User
from modules.database import Database
from modules.all_alert import All_alert

app = Flask(__name__)
app.secret_key = "test123"
Database.initialize()


@app.route('/')
def home():
    monen_dict, positon = Money.search_data()
    return render_template('home.html', money_dict=monen_dict, positon=positon)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['InputName']
        email = request.form['InputEmail']
        password = request.form['InputPassword']
        result = User.register_user(name, email, password)
        if result:
            session['email'] = email
            session['name'] = name
            return redirect('/')
        else:
            message = "该电子信箱已存在。"
            return render_template("register.html", message=message)
    else:
        return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['InputEmail']
        password = request.form['InputPassword']
        result = User.check_user(email, password)
        if result:
            session['email'] = email
            session['password'] = password
            return redirect('/')
        else:
            message = "邮箱或密码错误！"
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session['email'] = None
    session['password'] = None
    return redirect('/')


@app.route('/new_alert', methods=["GET", "POST"])
def new_alert():
    if session['email']:
        monen_dict, positon = Money.search_data()
        if request.method == 'POST':
            input_currency = request.form['input_currency']
            rate_exchange = request.form['rate_exchange']
            bank_buy = request.form['bank_buy']
            bank_sale = request.form['bank_sale']
            result = All_alert.create_alert(session['email'], input_currency, rate_exchange, [bank_buy, bank_sale])
            if result:
                message = "您的通知已经设置成功，可继续新增！"
                currency_msg = f"币别：{input_currency}"
                exchange_msg = "汇率：{}".format("现金汇率" if rate_exchange == "cash" else "即期汇率")
                buy_msg = f"银行买入通知价格：￥{bank_buy}"
                sale_msg = f"银行卖出通知价格：￥{bank_sale}"
                return render_template("new_alert.html", monen_dict=monen_dict, message=message,
                                       currency_msg=currency_msg, exchange_msg=exchange_msg,
                                       buy_msg=buy_msg, sale_msg=sale_msg)
            else:
                message = "您的通知新增失败，请重新新增！"
                currency_msg = f"币别：{input_currency}"
                exchange_msg = "汇率：{}".format("现金汇率" if rate_exchange == "cash" else "即期汇率")
                buy_msg = f"银行买入通知价格：￥{bank_buy}"
                sale_msg = f"银行卖出通知价格：￥{bank_sale}"
                return render_template("new_alert.html", monen_dict=monen_dict, message=message,
                                       currency_msg=currency_msg, exchange_msg=exchange_msg,
                                       buy_msg=buy_msg, sale_msg=sale_msg)
        else:
            return render_template("new_alert.html", monen_dict=monen_dict)
    else:
        return redirect('/login')


@app.route('/change_email', methods=['GET', 'POST'])
def change_email():
    if session['email']:
        if request.method == 'POST':
            new_email = request.form['InputNewEmail']
            password = request.form['InputPassword']
            result = User.check_user(session['email'], password)
            if result:
                User.update_user_email(session['email'], new_email)
                session['email'] = new_email
                message = f"您的邮箱已更新为{new_email}"
                return render_template("change_email.html", message=message)
            else:
                message = "您的密码错误！"
                return render_template("change_email.html", message=message)
        else:
            return render_template("change_email.html")
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
