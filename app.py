from flask import Flask, render_template, request, session, redirect
from modules.money import Money
from modules.user import User
from modules.database import Database


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


@app.route('/new_alert')
def new_alert():
    monen_dict, positon = Money.search_data()
    return render_template('new_alert.html', money_dict=monen_dict)


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
