import pandas as pd
from sklearn import tree
from sklearn.utils import shuffle

clf = tree.DecisionTreeClassifier(max_depth=7)
data = pd.read_csv('data.csv')
data.drop_duplicates()

pred_num = 100  # number of predicting sets
run_times = 20  # number of run times for calculating average accuracy


def run(times: int = 1):
    global data, clf
    sum_acc = 0

    for i in range(times):
        hit = 0
        data = shuffle(data)

        # devide the data into training and predicting sets
        X = data.iloc[0:-pred_num, 4:-1].values
        X_pred = data.iloc[-pred_num:, 4:-1].values
        Y = data['is_Private'].iloc[0:-pred_num].values
        Y_pred = data['is_Private'].iloc[-pred_num:].values

        # fit the model
        clf = clf.fit(X, Y)

        # test the model
        for j in range(len(X_pred)):
            if clf.predict([X_pred[j]]) == Y_pred[j]:
                hit += 1
                acc = hit/len(X_pred)*100
        sum_acc += acc
        print(f'#{i+1} accuracy:\t{round(acc, 2)}%')

    # calculate the average accuracy
    print('-'*22)
    print(f'avg accuracy:\t{round(sum_acc/times,2)}%')


if __name__ == '__main__':
    run(run_times)
