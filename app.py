from flask import Flask, render_template, request, session, redirect
from modules.money import Money
from modules.user import User
from modules.database import Database
from modules.all_alert import All_alert

app = Flask(__name__)
app.secret_key = "test123"


@app.before_first_request
def initialize():
    Database.initialize()
    session['email'] = session.get('email')
    session['name'] = session.get('name')


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
        money_dict, positon = Money.search_data()
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
                return render_template("new_alert.html", money_dict=money_dict, message=message,
                                       currency_msg=currency_msg, exchange_msg=exchange_msg,
                                       buy_msg=buy_msg, sale_msg=sale_msg)
            else:
                message = "您的通知新增失败，每个币种只能新增两种通知，请重新新增！"
                currency_msg = f"币别：{input_currency}"
                exchange_msg = "汇率：{}".format("现金汇率" if rate_exchange == "cash" else "即期汇率")
                buy_msg = f"银行买入通知价格：￥{bank_buy}"
                sale_msg = f"银行卖出通知价格：￥{bank_sale}"
                return render_template("new_alert.html", money_dict=money_dict, message=message,
                                       currency_msg=currency_msg, exchange_msg=exchange_msg,
                                       buy_msg=buy_msg, sale_msg=sale_msg)
        else:
            return render_template("new_alert.html", money_dict=money_dict)
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


@app.route('/cash_alert')
def cash_alert():
    if session['email']:
        cash_data = All_alert.find_user_alert(session['email'], "cash")
        return render_template('cash_alert.html', cash_data=cash_data)
    else:
        return redirect('/login')


@app.route('/sign_alert')
def sign_alert():
    if session['email']:
        sign_data = All_alert.find_user_alert(session['email'], "sign")
        return render_template('sign_alert.html', sign_data=sign_data)
    else:
        return redirect('/login')


@app.route('/update_alert', methods=['POST'])
def update_alert():
    if request.method == "POST":
        bank_buy = request.form['bank_buy']
        bank_sale = request.form['bank_sale']
        currency = request.form['currency']
        rate_exchange = request.form['rate_exchange']
        if rate_exchange == 'cash':
            All_alert.update_user_alert(session['email'], currency, rate_exchange, [bank_buy, bank_sale])
            return redirect('/cash_alert')
        else:
            All_alert.update_user_alert(session['email'], currency, rate_exchange, [bank_buy, bank_sale])
            return redirect('/sign_alert')


@app.route('/delete_alert', methods=['POST'])
def delete_alert():
    if request.method == "POST":
        currency = request.form['currency']
        rate_exchange = request.form['rate_exchange']
        if rate_exchange == 'cash':
            All_alert.delete_user_alert(session['email'], currency, rate_exchange)
            return redirect('/cash_alert')
        else:
            All_alert.delete_user_alert(session['email'], currency, rate_exchange)
            return redirect('/sign_alert')


if __name__ == '__main__':
    app.run(debug=True)
