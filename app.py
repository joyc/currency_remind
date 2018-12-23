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


if __name__ == '__main__':
    app.run(debug=True)
