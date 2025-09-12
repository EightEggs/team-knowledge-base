import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

data = pd.read_csv('MP.csv')
select1=data.columns[1:-1]
x=data[select1]
y=data['MP']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.02)
rfr = RandomForestRegressor(n_estimators=200, max_depth=50, n_jobs=-1)

if __name__ == '__main__':
    rfr.fit(x_train,y_train)
    print(rfr.score(x_test, y_test))
    y_pred = rfr.predict(x_test)
    print(list(y_test)-y_pred)

