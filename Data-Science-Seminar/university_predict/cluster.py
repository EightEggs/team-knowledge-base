import pandas as pd
from sklearn.cluster import AgglomerativeClustering as Agg
from sklearn.cluster import Birch, KMeans

clusters = []
clusters.append(KMeans(n_clusters=2))
clusters.append(Agg(n_clusters=2, affinity='cosine', linkage='complete'))
clusters.append(Birch(n_clusters=2))

data = pd.read_csv('data.csv')
data.drop_duplicates()
vect = data.iloc[:, 4:-1]

hit = 0

if __name__ == '__main__':
    for cluster in clusters:
        cl = cluster.fit_predict(vect)
        for i in range(len(data)):
            if cl[i] == cl[0] and data['is_Private'][i] == True:
                hit += 1
            if cl[i] == 1-cl[0] and data['is_Private'][i] == False:
                hit += 1

        print(f'{cluster.__class__.__name__}: {round(hit/len(data)*100, 2)}%')
        hit = 0
