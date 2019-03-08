import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from Q_3 import Search_Time
from Q_2 import generate_image
import numpy as np

### Q_1 of Assignment 2 CS789: Computational Cognitive Science Even Semester 2018-19 ###
### Group Members: Ravi (150572), Akarsh Gajbhiye (150067), Pranjal Giri (150505) ###

def main():
    no_shapes = 15
    time_list_feature = []
    time_list_conjunction = []
    img_size = 512

    for i in range(3, no_shapes):
        im = Image.new('RGB', (img_size, img_size))
        filled = np.zeros((img_size,img_size))
        draw = ImageDraw.Draw(im)
        points = (0,0),(0,img_size-1),(img_size-1,img_size-1),(img_size-1,0)
        labels = generate_image(draw, img_size = img_size,no_shapes = i,exp_type = 'f')
        indices = []
        for j in range(0, len(labels), 2):
            indices.append((labels[j], labels[j+1]))
        indices = [(t[0]-5, t[1]-5) for t in indices]
        time_list_feature.append(Search_Time(im, indices))

    for i in range(3, no_shapes):
        im = Image.new('RGB', (img_size, img_size))
        filled = np.zeros((img_size,img_size))
        draw = ImageDraw.Draw(im)
        points = (0,0),(0,img_size-1),(img_size-1,img_size-1),(img_size-1,0)
        labels = generate_image(draw, img_size = img_size,no_shapes = i,exp_type = 'c')
        indices = []
        for j in range(0, len(labels), 2):
            indices.append((labels[j], labels[j+1]))
        indices = [(t[0]-5, t[1]-5) for t in indices]
        time_list_conjunction.append(Search_Time(im, indices))
    plt.plot(range(3, no_shapes), time_list_feature)
    plt.plot(range(3, no_shapes), time_list_conjunction)
    plt.show()


if __name__=="__main__":
    main()
