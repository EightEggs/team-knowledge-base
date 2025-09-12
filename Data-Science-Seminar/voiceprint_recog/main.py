import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

data = pd.read_csv('voice.csv')
x = data.iloc[:, 0:-1]
y = data.iloc[:, -1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15)

svmc = svm.SVC(kernel='linear', C=7.0)
rfc = RandomForestClassifier(n_estimators=200, max_depth=50, n_jobs=-1)

if __name__ == '__main__':
    svmc.fit(x_train, y_train)
    rfc.fit(x_train, y_train)
    print(f"SVM: {round(svmc.score(x_test, y_test), 4)*100}%")
    print(f"RFC: {round(rfc.score(x_test, y_test), 4)*100}%")
