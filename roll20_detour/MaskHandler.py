import matplotlib.pyplot as plt
import numpy as np
from utils import get_img_name
import cv2

class MaskHandler:

    def __init__(self, num_class, alpha2color = None):
        if num_class<2:
           raise  ValueError('Minimum number of class must be higher or equal than 2.')
        self.num_class = num_class
        if alpha2color is None:
            self.ALPHA2COLOR, self.COLOR2ALPHA = self.getAutoAlphaColorMapping(self.num_class-1)
        else:
            assert(num_class == len(list(alpha2color.keys())))
            self.ALPHA2COLOR = alpha2color
            self.COLOR2ALPHA = {v: k for k, v in self.ALPHA2COLOR.items()}

    def getAutoAlphaColorMapping(self, num_class):
        '''
        Build two dictionaries :
        - Alpha pixel value to Blue value (used to build the mask)
        - Blue pixel value to alpha pixel value (used when unmasking)
        '''
        color_bin = 255/num_class
        alpha_bin = 1/num_class
        ALPHA2COLOR = dict()
        COLOR2ALPHA = dict()
        for i in range(num_class):
            ALPHA2COLOR[(i+1)*alpha_bin] = (i+1)*color_bin
            COLOR2ALPHA[(i+1)*color_bin] = (i+1)*alpha_bin
        ALPHA2COLOR[0] = 0
        COLOR2ALPHA[0] = 0 
        return ALPHA2COLOR, COLOR2ALPHA 

    def convert2blue(self, mat_img_src):
        '''
        Convert RGBA input image to a blue image
        '''
        r, g, b, a = np.rollaxis(mat_img_src, axis=-1)
        zeros = np.zeros([mat_img_src.shape[0],mat_img_src.shape[1] ])
        blues = np.zeros([mat_img_src.shape[0],mat_img_src.shape[1] ])
        count = 0
        for c in sorted(list(self.ALPHA2COLOR.keys())):
            if count == 0 :
                blues[a == c] = self.ALPHA2COLOR[c]
                cMinusOne = c
                count +=1
            # If last iteration
            elif count == len(self.ALPHA2COLOR.keys()) - 1:
                blues[a > cMinusOne] = self.ALPHA2COLOR[c]
                count +=1
            # Any other iteration
            else:
                blues[(a <= c) & (a > cMinusOne)] = self.ALPHA2COLOR[c]
                cMinusOne = c
                count +=1
        return np.dstack([zeros, zeros, blues])/255

    def get_mask(self, src_img, display = False, save_path = None):
        '''
        Build blue-mask from source image, display and save options
        '''
        npsrc = plt.imread(src_img)
        if display:
            print('SRC:')
            plt.imshow(npsrc)
            plt.show()
        resized = cv2.resize(npsrc, (256, 256))
        mask = self.convert2blue(resized)
        if display : 
            print('MASK (%d classes):' %(self.num_class))
            plt.imshow(mask)
            plt.show()
        if save_path != None:
            plt.imsave(save_path, mask)
        return mask
    
    def unmask(self, img, mask, show = True, imgFromNpy = True, maskFromPredNpy = True, convertToColor = False,save_folder_path = None):
        '''
        Apply given mask on given input image with display and save options. 
        Input img/mask can be either direct paths or already loaded numpy arrays
        '''
        if not imgFromNpy:
            npimg = plt.imread(img,0)
        else:
             npimg = np.copy(img)
        if not maskFromPredNpy:
             npmask = plt.imread(mask,0)
        else:
            npmask0 = np.copy(mask)
            if convertToColor:
                npmask = self.convertPredNpyToBlueMask(npmask0)
            else:
                npmask= npmask0
        npimg = npimg.astype(int)/255
        npmask = npmask.astype(int)*255
        npimg = cv2.resize(npimg, (256, 256))
        alphas = np.zeros([npimg.shape[0], npimg.shape[1]])
        all_blues = npmask.max(axis = -1)
       
        for blue in sorted(list(self.COLOR2ALPHA.keys())):
            _temp_blue_idx = (all_blues==blue)
            alphas[_temp_blue_idx] = self.COLOR2ALPHA[blue]
        result = np.dstack((npimg, alphas)) 
        if show:
            plt.figure()
            plt.imshow(result)
        if save_folder_path is not None:
            plt.imsave(save_folder_path, result)
        return result

    def convertPredNpyToBlueMask(self, maskPredNpy):
        '''
        Convert Unet output prediction to a mask RGB image with a specific blue shade for each class
        '''
        self.COLOR2ALPHA[0] = 0
        _listed_keys = sorted(list(self.COLOR2ALPHA.keys()))
        zeros = np.zeros([maskPredNpy.shape[0],maskPredNpy.shape[1] ])
        blues = np.apply_along_axis(lambda x : _listed_keys[np.argmax(x)], -1, maskPredNpy)
        return np.dstack([zeros, zeros, blues])/255
            
    