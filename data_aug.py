#import helpers etc.
import utils.helper as helper
import numpy as np
import cv2
import os
import random
from matplotlib import pyplot as plt


# # Set seed for repeatable results
# seed = 40
# np.random.seed(seed)
# tf.random.set_seed(seed)

#get image and mask path 
# PATH_TRAIN_IMG, PATH_TRAIN_MASK, PATH_TEST_IMG, PATH_TEST_MASK = helper.data_paths()
# #get filenames of img and mask as list
# fnames_img = helper.get_fnames(PATH_TRAIN_IMG)
# fnames_mask = helper.get_fnames(PATH_TRAIN_MASK)
# #rebuild np arrays
# index = 40
# sample_img = helper.rebuild_npy(PATH_TRAIN_IMG/fnames_img[index])
# sample_mask = helper.rebuild_npy(PATH_TRAIN_MASK/fnames_mask[index])


#np arrays must be rebuilt
def rot90(image,mask):
    k = random.randint(1,3)
    new_img = np.rot90(image,k)
    new_mask = np.rot90(mask,k)
    return new_img,new_mask

#np arrays must be rebuilt
def flip_lr(image,mask):
    new_image = np.fliplr(image)
    new_mask = np.fliplr(mask)
    return new_image,new_mask

def flip_ud(image,mask):
    new_image = np.flipud(image)
    new_mask = np.flipud(mask)
    return new_image, new_mask

#blend 2 images together
def blend(img1,img2):
    alpha = 0.8 + random.random() * 0.4
    return (img1*alpha + (1-alpha)*img2).astype(np.uint8)

#grayscale image only
def grayscale(image):
    alpha = np.asarray([0.25,0.25,0.25]).reshape((1,1,3))
    return np.sum(alpha*image,axis=2,keepdims=True)

def saturation(image):
    gs = grayscale(image)
    return blend(image,gs)

def brightness(image):
    gs = np.zeros_like(image)
    return blend(image,gs)

def contrast(image):
    gs = grayscale(image)
    gs = np.repeat(gs.mean(),3)
    return blend(image,gs)

def gauss_noise(image):
    gauss = np.random.normal(10,10.0**0.5,image.shape).astype(np.uint8)
    new_image = np.copy(image)
    new_image+=gauss-np.min(gauss)
    return new_image

def gamma(image):
    gamma = 0.8+0.4*random.random()
    new_image = np.copy(image)
    new_image = np.clip(new_image,a_min=0.0,a_max=None)
    new_image = np.power(new_image,gamma).astype(np.uint8)
    return new_image

#Prob variables needed: rot90_prob,flipud_prob,fliplr_prob,color_aug(for brightness,
#contrast,saturation), gauss_prob, gamma_prob
def data_augment(image,mask,rot90_prob=0,flipud_prob=0,fliplr_prob=0,color_aug_prob=0,gauss_aug_prob=0,gamma_prob=0):
    if random.random() < rot90_prob:
        image,mask = rot90(image,mask)
    if random.random() < fliplr_prob:
        image,mask = flip_lr(image,mask)
    if random.random() < flipud_prob:
        image,mask = flip_ud(image,mask)
    if random.random() < color_aug_prob:
        image = saturation(image)
    if random.random() < color_aug_prob:
        image = brightness(image)
    if random.random() < color_aug_prob:
        image = contrast(image)
    if random.random() < gauss_aug_prob:
        image = gauss_noise(image)
    if random.random() < gamma_prob:
        image = gamma(image)

    return image,mask

# new_image = brightness(sample_img)
# #new_image,new_mask = data_augment(sample_img,sample_mask,0.5,0.5,0.5,0.5,0.5,0.5)
# print(new_image.shape)
# #print(new_mask.shape)
# print(new_image[0].dtype)
# #print(new_mask[0].dtype)
# plt.subplot(121),plt.imshow(sample_img),plt.title('Input')
# plt.subplot(122),plt.imshow(new_image),plt.title('Output')
# plt.show()