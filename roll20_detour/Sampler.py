import matplotlib.pyplot as plt
import cv2
import numpy as np

class Sampler :
    def __init__(self, mask_handler):
        self.mask_handler = mask_handler

    def is_eligible(self, img, rgba = False):
        img_mat = plt.imread(img,0)
        if len(img_mat.shape) < 3:
            print('Not MxNxC', img)
            return False
        if rgba:
            if img_mat.shape[2] != 4:
                print('Not RBGA', img)
                return False
        else:
            if img_mat.shape[2] != 3:
                print('Not RBG', img)
                return False
        return True
          
    def preprocessInput(self, img, mask= None):
        '''
        '''
        # Resize image to fit UNET
        img0 = cv2.resize(img, (256, 256))
        img0 = img0 / 255
        if mask is not None:
            # Take the Blue value of the loaded mask
            mask0 = mask[:,:,2]
            # For one pixel in the image, find the class in mask and convert it into one-hot vector
            new_mask = np.zeros(mask0.shape + (self.mask_handler.num_class,))
            c = 0
            for i in np.unique(mask0):
                new_mask[mask0 == i,c] = 1
                c+=1
            return (img0,new_mask)
        else:
            return img0
    
    def generateTrain(self, train_files, mask_files):
        '''
        '''
        image_arr = []
        mask_arr = []
        for index,item in enumerate(train_files): 
            if not (self.is_eligible(item)):
                continue 
            img = plt.imread(item,0) #TODO check hazard
            mask = plt.imread(mask_files[index])
            img2,mask2 = self.preprocessInput(img,mask)
            image_arr.append(img2)
            mask_arr.append(mask2)
        image_np =np.stack(image_arr, axis =0)
        mask_np = np.stack(mask_arr, axis =0)
        print('TRAIN:', image_np.shape)
        print('TARGET:', mask_np.shape)
        return image_np,mask_np

    def generateTest(self, test_files):
        '''
        '''
        size = len(test_files)
        c = 0
        test_arr = []
        for index,item in enumerate(test_files): 
            img = plt.imread(item,0)
            img2 = self.preprocessInput(img)
            test_arr.append(img2)
            c+=1
        image_np =np.stack(test_arr, axis = 0)
        return image_np

    
