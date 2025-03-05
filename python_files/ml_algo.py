import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import yfinance as yf

symbol = "GLD"
start = "2020-01-01"
end = "2024-12-31"

data = yf.download(symbol, start=start, end=end)["Close"]
data['return'] = data['GLD'].pct_change()
data.dropna(inplace=True)

lags = 5
columns = [f"lag_{lag}" for lag in range(1, lags+1)]
counter = 1
for column in columns:
    data[column] = data['return'].shift(counter)
    counter += 1
#data = data.dropna(inplace=True)
data = data[['GLD'] + columns + ['return']]
data.dropna(inplace=True)
data['direction'] = np.where(data['return'] > 0, 1, -1)
data[columns] = np.where(data[columns] > 0, 1, 0)
# print(data.head(6))

model = SVC(C=1, kernel='linear', gamma='auto', probability=True)
split = int(0.8 * len(data))
train = data.iloc[:split].copy()
model.fit(train[columns], train['direction'])
win = accuracy_score(train['direction'], model.predict(train[columns]))
#print(f"Training accuracy: {win}")

test = data.iloc[split:].copy()
test['prediction'] = model.predict(test[columns])
#print(test)
test_win = accuracy_score(test['direction'], test['prediction'])
#print(f"Test accuracy: {test_win:.2f}")

forecast = data.iloc[-1][columns].to_list()
forecast.pop()
direction = 1.0 if data['return'].iloc[-1] > 0 else 0.
forecast.insert(0, direction)
forecast = pd.DataFrame(forecast, columns).T
print(forecast)
print(model.predict(forecast)[0])
