import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import yfinance as yf


class ML:
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None
        self.lags = 5
        self.columns = [f"lag_{lag}" for lag in range(1, self.lags+1)]
        self.model = SVC(C=1, kernel='linear', gamma='auto', probability=True)

    def download_data(self):
        self.data = yf.download(self.symbol, start=self.start, end=self.end)["Close"]
        self.data['return'] = self.data[self.symbol].pct_change()
        self.data.dropna(inplace=True)

    def create_lags(self):
        counter = 1
        for column in self.columns:
            self.data[column] = self.data['return'].shift(counter)
            counter += 1
        self.data = self.data[['GLD'] + self.columns + ['return']]
        self.data.dropna(inplace=True)

    def create_direction(self):
        self.data['direction'] = np.where(self.data['return'] > 0, 1, -1)
        self.data[self.columns] = np.where(self.data[self.columns] > 0, 1, 0)

    def train(self):
        split = int(0.8 * len(self.data))
        train = self.data.iloc[:split].copy()
        self.model.fit(train[self.columns], train['direction'])
        win = accuracy_score(train['direction'], self.model.predict(train[self.columns]))
        return win

    def test(self):
        split = int(0.8 * len(self.data))
        test = self.data.iloc[split:].copy()
        test['prediction'] = self.model.predict(test[self.columns])
        test_win = accuracy_score(test['direction'], test['prediction'])
        return test_win

    def forecast(self):
        forecast = self.data.iloc[-1][self.columns].to_list()
        forecast.pop()
        direction = 1.0 if self.data['return'].iloc[-1] > 0 else 0.
        forecast.insert(0, direction)
        forecast = pd.DataFrame(forecast, self.columns).T
        return self.model.predict(forecast)[0]

if __name__ == "__main__":
    ml = ML("GLD", "2020-01-01", "2024-12-31")
    ml.download_data()
    ml.create_lags()
    ml.create_direction()
    win = ml.train()
    print(f"Training accuracy: {win}")
    test_win = ml.test()
    print(f"Test accuracy: {test_win:.2f}")
    forecast = ml.forecast()
    print(forecast)