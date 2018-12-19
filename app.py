from flask import Flask, render_template
from modules.money import Money

app = Flask(__name__)


@app.route('/')
def home():
    monen_dict, positon = Money.search_data()
    return render_template('home.html', money_dict=monen_dict, positon=positon)


if __name__ == '__main__':
    app.run(debug=True)
