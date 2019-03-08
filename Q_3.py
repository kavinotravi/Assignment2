from PIL import Image
import numpy as np
import argparse
from Q_1 import detect_shape

### Q_3 of Assignment 2 CS789: Computational Cognitive Science Even Semester 2018-19 ###
### Group Members: Ravi (150572), Akarsh Gajbhiye (150067), Pranjal Giri (150505) ###

def get_indices(file):
    start = file.index('[')
    end = file.index(']')
    temp = file[start+1: end].split(",")
    temp1 = [int(i) for i in temp]
    indices = []
    for j in range(0, len(temp1), 2):
        indices.append((temp1[j], temp1[j+1]))
    indices = [(t[0]-5, t[1]-5) for t in indices]
    return indices

def Search_Time(img, indices):
    # Detect Shapes
    shapes = []
    for pos in indices:
        cropped = (pos[0], pos[1], pos[0] + 60, pos[1] + 60)
        cropped_im = img.crop(cropped)
        shapes.append(detect_shape(cropped_im.convert('L')))

    # Detect colors
    color = []
    img_as_array = np.array(img)
    Time = 0
    for pos in indices:
        color.append(np.argmax(img_as_array[pos[1]+10, pos[0] + 5]))
    if len(set(color))<=1 & len(set(shapes))<=1:
        print("All are same")
    elif ((len(set(color))<=1) & (len(set(shapes))>1)):
        # Feature Search with different shapes
        print("Feature Search")
        if np.sum(shapes)==1:
            loc = shapes.index(1) # Find the Location of Square
            index = indices[loc]
            print("The odd one out is Square at ({}, {})".format(index[0] -5, index[1] - 5))
        else:
            loc = shapes.index(0) # Find the Location of Triangle
            index = indices[loc]
            print("The odd one out is Triangle at ({0}, {1})".format(index[0] -5, index[1] - 5))
            Time = 1
    elif ((len(set(shapes))<=1) & (len(set(color))>1)):
        # Feature search with different colors
        print("Feature Search")
        if np.sum(color)==2:
            loc = color.index(2) # Find the Location of Blue
            index = indices[loc]
            print("The odd one out is Blue at ({0}, {1})".format(index[0] -5, index[1] - 5))
        else:
            loc = color.index(0) # Find the Location of Red
            index = indices[loc]
            print("The odd one out is Red at ({0}, {1})".format(index[0] -5, index[1] - 5))
            Time = 1
    else:
        # Conjunction search
        print("Conjunction Search")
        Counter = {"Red Square": 0, "Red Triangle":0, "Blue Square":0, "Blue Triangle": 0}
        Track = {}
        for i in range(len(indices)):
            Time += 1
            if color[i]==0:
                if shapes[i]==1:
                    Counter["Red Square"] += 1
                    Track["Red Square"] = (indices[i][0] - 5, indices[i][1] - 5)
                elif shapes[i]==0:
                    Counter["Red Triangle"] += 1
                    Track["Red Triangle"] = (indices[i][0] - 5, indices[i][1] - 5)
            elif color[i]==2:
                if shapes[i]==1:
                    Counter["Blue Square"] += 1
                    Track["Blue Square"] = (indices[i][0] - 5, indices[i][1] - 5)
                elif shapes[i]==0:
                    Counter["Blue Triangle"] += 1
                    Track["Blue Triangle"] = (indices[i][0] - 5, indices[i][1] - 5)
        #print(Counter)
        for x in Counter:
            if Counter[x]==1:
                print("The odd one out is {0} at ({1}, {2})".format(x, Track[x][0], Track[x][1]))
                break
    print("Time Required is {} timesteps".format(Time))
    return Time

def main(file):
    img = Image.open(file)
    indices = get_indices(file)
    _ = Search_Time(img, indices)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str,
                        help='The Location of the file. Assumed images were generated from Q_2 and they were not modified after that inlcuding name')
    args = parser.parse_args()
    main(args.file)
