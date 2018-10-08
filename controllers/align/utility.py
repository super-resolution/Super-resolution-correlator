import cv2
import numpy as np
import pyqtgraph.opengl as gl
import pyqtgraph as pg
from controllers.align import CudaAlphaShape as alpha
from controllers.align.CudaHough import hough_transform
from skimage import transform
from scipy.stats import pearsonr
from PyQt5.QtCore import QPoint


#app = pg.mkQApp()



def find_mapping(image, c_template, n_col=5, n_row=5):
    results = []
    overlay = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_GRAY2RGBA)
    image = image.astype(np.uint8)
    template = cv2.cvtColor(c_template.astype(np.uint8), cv2.COLOR_RGBA2GRAY)

    H = hough_transform()
    H.set_image(image)

    #im = im.astype("uint8")
    #imgs_t = []
    points1 = []
    points2 = []
    overlay = overlay.astype(np.uint16)
    for i in range(n_col):
        for j in range(n_row):
            k,j = 0+j*200,200+j*200
            l,m = i*200,200+i*200
            points1.append(np.array((k+100,l+100)))
            template_segment = template[k:j,l:m]
            imnew = c_template[k:j,l:m]
            H.set_template(template_segment)
            try:
                res = H.transform()
            except:
                print("r-table fail")
            results.append(res[0:2])
            points2.append(res[1][0:2])

            #imgs_t.append(imnew)
            #paint segments in image
            try:
                M = cv2.getRotationMatrix2D((imnew.shape[0] / 2, imnew.shape[1] / 2), res[0], 1)
                imnew = cv2.warpAffine(imnew, M, (imnew.shape[0], imnew.shape[1]))
                for h in range(200):
                    for k in range(200):
                        overlay[2*res[1][0]-100+h,2*res[1][1]-100+k] += imnew[h,k,0:4]
            except: print("image out of bounds")
    return points1,points2,overlay,results#todo:result wrapper


def error_management(result_list, points1, points2, n_row = 5):
    num = []
    for i,ent1 in enumerate(result_list):#todo: write function
        row1 = int(i/n_row)
        col1 = i%n_row
        max=0
        print(i)
        for j,ent2 in enumerate(result_list):
            row2 = int(j/n_row)
            col2 = j%n_row
            val1 = ent1[1][0]-(col1-col2)*100*np.cos(np.deg2rad(ent1[0]))+(row1-row2)*100*np.sin(np.deg2rad(ent1[0]))
            val2 = ent1[1][1]-(row1-row2)*100*np.cos(np.deg2rad(ent1[0]))-(col1-col2)*100*np.sin(np.deg2rad(ent1[0]))
            if np.absolute(val1-ent2[1][0])<14 and np.absolute(val2-ent2[1][1])<14:#todo: tangens
                print(True)
                max+=1
            else:
                print(False)
        if max>4:
            num.append(i)
    points1 = np.asarray(points1)
    points2 = np.asarray(points2)
    points1 = points1[np.array(num)]
    points2 = points2[np.array(num)]
    print(points1, points2)
    p1 = np.fliplr(points1)
    p2 = np.float32(points2)*2
    p2 = np.fliplr(p2)
    return p1,p2

def test_pearson(sim, dstorm, map):

    mask = np.ones_like(dstorm).astype(np.float32)
    binary_mask = transform.warp(mask, inverse_map=map.inverse).astype(np.bool)

    dstorm_warped = transform.warp(dstorm, inverse_map=map.inverse)
    masked_dstorm = np.ma.array(data=dstorm_warped, mask=np.logical_not(binary_mask))#

    masked_sim = np.ma.array(data=sim, mask=np.logical_not(binary_mask))
    masked_mask = np.ma.array(data=binary_mask, mask=np.logical_not(binary_mask))
    corr_coef = pearsonr(masked_dstorm.flatten(),masked_sim.flatten())
    print("image:",corr_coef)#masked correlation only compare visible parts
    cut_sim_masked = (sim*binary_mask).astype(np.uint8)
    #print("mask:",pearsonr(binary_mask.flatten()*255, cut_sim_masked.flatten()))#unmasked correlation to white
    return corr_coef