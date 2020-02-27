import os
import argparse
from keras.models import load_model

from MaskHandler import MaskHandler
from Sampler import Sampler
from Unet import Unet
from utils import list_repo, copy_dir, get_img_name
'''
# EXAMPLE OF CMD CALL ##
python detour_cmd.py --src '**PATH_SRC**/roll20_scrapper/scrapping_results/' --tgt '**PATH_TGT**/roll20_detour/predictions/' --model '**PATH_MODEL**/roll20_detour/model/unet_2_06.h5'
'''

'''
CONFIG
'''
NUM_CLASS = 2

parser = argparse.ArgumentParser(description='Detour scrapped ROLL20 png images with a pre-trained model')
parser.add_argument('--src', type = str, help='Source folder where the scrapped images to detour are located')
parser.add_argument('--tgt', type = str, help='Target folder to save the inferences')
parser.add_argument('--model', type = str, help='Pre-trained model to use for the inference')

def main():
    
    args = parser.parse_args()
    if args.src is None:
        raise Exception('No source path has been given')
    if args.src is None:
        raise Exception('No target path has been given')

    folders = list_repo(args.src, onlyRepo = True)

    copy_dir(args.src, args.tgt)

    alpha2color = {0.85 : 0, 1 : 255}
    masker = MaskHandler(NUM_CLASS, alpha2color)
    sampler = Sampler(masker)
    unet = Unet(NUM_CLASS)

    unet.model = load_model(args.model)
    print('Model loaded')

    for f in folders:
        print('##')
        print(f)
        print('##')
        im_infer = list_repo(args.src+f+'/')
        print('Found', len(im_infer), 'images to detour')
        eligible = [img for img in im_infer if sampler.is_eligible(img)]
        z = sampler.generateTest(eligible)
        print('Images prepared for inference')
        inference = unet.model.predict(z)
        for IDX in range(inference.shape[0]):
            print('Prediction', IDX+1, 'done')
            unmasked = masker.unmask(eligible[IDX], inference[IDX], show = False, imgFromNpy = False, maskFromPredNpy = True,convertToColor =True, save_folder_path = args.tgt+get_img_name(eligible[IDX])+'.png')

if __name__ == "__main__":
    main()