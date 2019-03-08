import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as nd
from PIL import Image, ImageDraw,ImageFont
from random import randint
import argparse

### Q_2 of Assignment 2 CS789: Computational Cognitive Science Even Semester 2018-19 ###
### Group Members: Ravi (150572), Akarsh Gajbhiye (150067), Pranjal Giri (150505) ###

#Function to draw triangle
def draw_triangle(draw, x,y,size,color):
    x1 = x;  y1 = y
    x2 = x+size; y2 = y
    x3 = x; y3 = y+size
    points = (x1,y1),(x2,y2),(x3,y3)
    if color == 'Blue':
        cm = (0,0,255)
    elif color == 'Red':
        cm = (255,0,0)
    draw.polygon(points, fill = cm)

#Function to draw Rectangle
def draw_rectangle(draw, x,y,size,color):
    x1 = x; y1 = y
    x2 = x+size; y2 = y
    x3 = x+size; y3 = y+size
    x4 = x; y4 = y+size
    points = (x1,y1),(x2,y2),(x3,y3),(x4,y4)
    if color == 'Blue':
        cm = (0,0,255)
    elif color == 'Red':
        cm = (255,0,0)
    draw.polygon(points, fill = cm)

#Function to calculate the coordinates for the shapes generated
def generate_image(draw, img_size,no_shapes,exp_type):
    filled = np.zeros((512,512))		#tracking filled indices
    size = 50
    error = 0
    labels = []
    max_trials = 25
    for i in range(max_trials):
        x1 = randint(0, 511)
        y1 = randint(0, 511)
        if x1 < (img_size-size-5) and y1 < (img_size-size-5):
            pass
        else:
            continue
        draw_triangle(draw, x = x1,y=y1,size = 50, color = 'Red')
        labels.append(x1)
        labels.append(y1)
        for j in range(x1-5,x1+size+5):
            for k in range(y1-5,y1+size+5):
                filled[j,k] = 1
        break
    if exp_type == 'f':
        if (randint(1,100)%2) == 0:
            col = 'Red'
            shap = 'sqr'
        else:
            col = 'Blue'
            shap = 'triangle'
        for i in range(no_shapes - 1):
            for j in range(max_trials):
                x1 = randint(0, 511)
                y1 = randint(0, 511)
                if x1 < (img_size-size-5) and y1 < (img_size-size-5):
                    pass
                else:
                    continue
                flag = 0
                for k in range(x1-5,x1+size+5):
                    for l in range(y1-5,y1+size+5):
                        if filled[k,l] == 1:
                            flag = 1
                if flag == 0:
                    for k in range(x1-5,x1+size+5):
                        for l in range(y1-5,y1+size+5):
                            filled[k,l] = 1
#storing the xy coordinates of top-left corner of each shape
                    labels.append(x1)
                    labels.append(y1)
                    if col == 'Red':
                        draw_rectangle(draw, x = x1,y=y1,size = 50, color = 'Red')
                    else :
                        draw_triangle(draw, x = x1,y=y1,size = 50, color = 'Blue')
                    break
                if j == max_trials-1:
                    print('Could not fit required number of images in given trials')
                    error = 1
                    return
    if exp_type == 'c':
        for i in range(no_shapes - 1):
            if (randint(1,100)%2) == 0:
                col = 'Red'
                shap = 'sqr'
            else:
                col = 'Blue'
                shap = 'triangle'
            for j in range(max_trials):
                x1 = randint(0, 511)
                y1 = randint(0, 511)
                if x1 < (img_size-size-5) and y1 < (img_size-size-5):
                    pass
                else:
                    continue
                flag = 0
                for k in range(x1-5,x1+size+5):
                    for l in range(y1-5,y1+size+5):
                        if filled[k,l] == 1:
                            flag = 1
                if flag == 0:
                    for k in range(x1-5,x1+size+5):
                        for l in range(y1-5,y1+size+5):
                            filled[k,l] = 1
                    labels.append(x1)
                    labels.append(y1)
                    if col == 'Red' and shap == 'sqr':
                        draw_rectangle(draw, x = x1,y=y1,size = 50, color = 'Red')
                    elif col == 'Blue' and shap == 'triangle' :
                        draw_triangle(draw, x = x1,y=y1,size = 50, color = 'Blue')
                    elif col == 'Blue' and shap == 'sqr' :
                        draw_rectangle(draw, x = x1,y=y1,size = 50, color = 'Blue')
                    break
                if j == max_trials-1:
                    print('Could not fit required number of images in given trials')
                    error = 1
                    return
    if error == 0:
        return labels

def main(exp_type, no_shapes):
    img_size = 512
    im = Image.new('RGB', (img_size, img_size))
    filled = np.zeros((img_size,img_size))
    draw = ImageDraw.Draw(im)
    points = (0,0),(0,img_size-1),(img_size-1,img_size-1),(img_size-1,0)
    #draw.polygon(points , fill = (255,255,255))
    labels = generate_image(draw, img_size = img_size,no_shapes = no_shapes,exp_type = exp_type)
    label_str = [str(i) for i in labels]
    stri = "Experiment:_" + str(exp_type) + "_Objects:" + str(no_shapes)+"labels"+ "[" + ",".join(label_str) + "]" + ".jpg"
    #plt.imshow(im)
    im.save(stri)
    #saving generated image with appropriate name
    print(labels)
    plt.imshow(im)

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('exp_type', type=str,
                        help='The type of Image search conjunction(c) or feature search(f)')
    parser.add_argument('no_shapes', type=str,
                        help="The no of shapes")
    args = parser.parse_args()
    main(args.exp_type, int(args.no_shapes))
