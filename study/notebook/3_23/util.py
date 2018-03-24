from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.cluster import KMeans
class Image():
    indexs = np.array([])
    def __init__(self,path):
        self.path = path;
        self.image = misc.imread(path)

    def returnImage(self):
        return self.image
    def showImage(self):
        plt.imshow(self.image)
        plt.show()
    def filter(self,condition):
        if type(condition)==str:
            self.indexs =  np.array(np.where(eval(condition)))
        else:
            return "Please give the condition as String"
    def drawRect(self,point,width,height,title=""):
        fig,ax = plt.subplots(1);
        ax.imshow(self.image)
        rect = patches.Rectangle(point,width,height,linewidth=1,edgecolor="r",facecolor="none")
        ax.add_patch(rect)
        plt.title(title)
        plt.show()

    def returnMinMax(self):
        height = self.indexs[0]
        width = self.indexs[1]
        return np.array([min(width),max(width),min(height),max(height)])

    def calArea(self):
        result = self.returnMinMax()
        width = result[1] - result[0]
        height = result[3] - result[2]
        return np.array([width,height])

    def centroid(self,n_clusters):
        real = self.indexs[0:2]
        points =[]
        for i in range(real.shape[1]):
            points.append([real[0,i],real[1,i]])
        self.data = np.vstack({tuple(row) for row in np.array(points)})
        self.kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=5)
        self.kmeans.fit(self.data)
        centroids = self.kmeans.cluster_centers_
        return centroids
    def predict(self):
        return self.kmeans.predict(self.data)
    def imageTemplate(self):
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]