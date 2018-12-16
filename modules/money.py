import pandas


class Money:
    def __init__(self, currency, currency_cn, cash_in, cash_out, sign_in, sign_out):
        self.currency = currency
        self.currency_cn = currency_cn
        self.cash_in = cash_in
        self.cash_out = cash_out
        self.sign_in = sign_in
        self.sign_out = sign_out

    @staticmethod
    def search_data():
        data = pandas.read_html('https://rate.bot.com.tw/xrt?Lang=zh-CN')[0]
        currency_table = data.ix[:, 0:5]
        currency_table.columns = ['币别', '现金汇率-买入', '现金汇率-卖出', '即期汇率-买入', '即期汇率-卖出', ]
        currency_cn = currency_table['币别'].str.extract("(\w+)", expand=True)     # 中文币别名
        currency_table['币别'] = currency_table['币别'].str.extract("\((\w+)\)", expand=True)   # 英文币别名
        money_dict = {}
        position = {}
        for i in range(0, 19):
            dollar = currency_table.values[i]
            money_dict[i] = Money(dollar[0], currency_cn.values[i][0], dollar[1], dollar[2], dollar[3], dollar[4])
            position[currency_cn.values[i][0]] = i
        # print(currency_table.values[0])
        return money_dict, position


# for test
# money_dict, position = Money.search_data()
# for i in range(0, 19):
#     print(money_dict[i].currency)
#     print(money_dict[i].currency_cn)
#     print(money_dict[i].cash_in)
#     print(money_dict[i].cash_out)
#     print(money_dict[i].sign_in)
#     print(money_dict[i].sign_out)
#     print('--------')
