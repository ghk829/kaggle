import util
from util import Image
import numpy as np
import matplotlib.pyplot as plt
def main():
    image = Image("image.png")
    # image.image = image.image[50:210][:,170:280,:]
    image.filter("self.image!=255")
    width = image.calArea()[0]
    height = image.calArea()[1]
    print(image.centroid(5))
    plt.scatter(image.data[:,0],image.data[:,1],c=image.predict())
    plt.show()
    # area = width * height
    # image.drawRect((image.returnMinMax()[0], image.returnMinMax()[2]), width, height, "Area : " + str(area))
if __name__=="__main__":
    main();