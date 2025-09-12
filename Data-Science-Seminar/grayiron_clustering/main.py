from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN

# Read the image
img = Image.open('sample.jpg').convert('RGB')
img = np.array(img)
m, n, d = img.shape

# For clustering the image using k-means, we first need to convert it into a 2-dimensional array
image_2D = img.reshape(m*n, d)
for i in range(m):
    if image_2D[i][0] < 130:
        image_2D[i] = np.repeat(130, d)
    if image_2D[i][0] > 165:
        image_2D[i] = np.repeat(165, d)

# Use KMeans clustering algorithm from sklearn.cluster to cluster pixels in image
cl = KMeans(n_clusters=3, random_state=0).fit(image_2D).labels_

# Reshape back the image from 2D to 3D image
clustered_3D = cl.reshape(m, n)

plt.imshow(clustered_3D, cmap='bone')
plt.title('Clustered Image')
plt.show()
