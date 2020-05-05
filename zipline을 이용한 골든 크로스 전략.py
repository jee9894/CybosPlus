import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
from zipline.api import order_target, record, symbol
from zipline.algorithm import TradingAlgorithm

def initialize(context):
    context.i = 0
    context.sym = symbol('AAPL')
    context.hold = False

def handle_data(context, data):
    context.i += 1
    if context.i < 20:
        return

    buy = False
    sell = False

    # 5일 이동평균선과 20일 이동평균선 구함
    ma5 = data.history(context.sym, 'price', 5, '1d').mean()
    ma20 = data.history(context.sym, 'price', 20, '1d').mean()

    # 주식을 보유하지 않는 상태에서 골든크로스가 발생하면 100주 매수
    if ma5 > ma20 and context.hold == False:
        order_target(context.sym, 1)
        context.hold = True
        buy = True
    # 주식을 보유한 상태에서 데드크로스가 발생하면 100주를 매도
    elif ma5 < ma20 and context.hold == True:
        order_target(context.sym, -1)
        context.hold = False
        sell = True

    record(AAPL=data.current(context.sym, "price"), ma5=ma5, ma20=ma20, buy=buy, sell=sell)

start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2020, 5, 1)
data = web.DataReader("AAPL", "yahoo", start, end)

# 수정종가 칼럼만 가져옴
data = data[['Adj Close']]
data.columns = ["AAPL"]
data = data.tz_localize("UTC")

algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
result = algo.run(data)

# 수익률
# plt.plot(result.index, result.portfolio_value)
# plt.show()

# 이동평균선과 매수 매도 시점
plt.plot(result.index, result.ma5)
plt.plot(result.index, result.ma20)
plt.legend(loc='best')

plt.plot(result.ix[result.buy == True].index, result.ma5[result.buy == True], '^')
plt.plot(result.ix[result.sell == True].index, result.ma5[result.sell == True], 'v')
plt.show()