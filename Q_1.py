#Importing required packages

from PIL import Image
import numpy as np
from scipy import ndimage as nd
import argparse
from skimage.util import img_as_float
from skimage.filters import gabor_kernel

### Q_1 of Assignment 2 CS789: Computational Cognitive Science Even Semester 2018-19 ###
### Group Members: Ravi (150572), Akarsh Gajbhiye (150067), Pranjal Giri (150505) ###

def generate_features(image, kernel, kernel1):
    """
    args - Image, Kernel and kernel1 with offset pi/2
    returns - Feature for a given filter
    """
    # Normalize images for better comparison.
    image = (image - image.mean()) / image.std()
    return np.sqrt(nd.convolve(image, np.real(kernel), mode='wrap')**2 +
                   nd.convolve(image, np.imag(kernel), mode='wrap')**2 + np.sqrt(nd.convolve(image, np.real(kernel1), mode='wrap')**2 +
                   nd.convolve(image, np.imag(kernel1), mode='wrap')**2))

def check_triangle(features):
    """
    args - Feature vector (list of matrices)
    returns - 1 if triangle 0 otherwise
    """
    M = features[0].shape[0]
    #45-degree edge
    sum_edge1 = np.sum([features[1][M-1-i, i] for i in range(M)])
    #90-degree edge
    sum_edge2 = np.sum(features[2][5])
    #45-degree edge
    sum_edge3 = np.sum(features[0][:, 5])
    if (sum_edge1 > 25) & (sum_edge2 > 25) & (sum_edge3 > 25):
        return 1 # Is triangle
    else:
        return 0

def check_square(features):
    """
    args - Feature vector (list of matrices)
    returns - 1 if square 0 otherwise
    """
    M = features[0].shape[0]

    sum_edge1 = np.sum(features[2][5])		#90-degree edges
    sum_edge2 = np.sum(features[2][-5])

    sum_edge3 = np.sum(features[0][:, 5])	#0 -degree edges
    sum_edge4 = np.sum(features[0][:, -5])

    if (sum_edge1 > 25) & (sum_edge2 > 25) & (sum_edge1 > 25) & (sum_edge2 > 25):
        return 1 # Is square
    else:
        return 0

def detect_shape(Image):
    """
    args - image
    returns - 1 if triangle 2 if square and 0 otherwise
    """
    img = img_as_float(Image)
    features = []
    for theta in (0, np.pi/4.0, np.pi/2.0):
	   #3 filtersimplemented
        kernel = gabor_kernel(0.1, theta=theta, offset = 0)
        kernel1 = gabor_kernel(0.1, theta, offset = np.pi/2.0)
        features.append(generate_features(img, kernel, kernel1))
    if check_triangle(features)==1:
        return 0 # For triangle
    elif check_square(features)==1:
        return 1 # For Square
    else:
        return 2 # Neither of them

def main(file):
    img = Image.open(file).convert('L')
    out = detect_shape(img)
    if out==0:
        print("Triangle")
    elif out==1:
        print("Square")
    else:
        print("Neither a Square nor Triangle")

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('Image_location', type=str,
                        help='Path to Image. Image must be 60x60')
    args = parser.parse_args()
    main(args.Image_location)
