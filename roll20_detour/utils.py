import os
import matplotlib.pyplot as plt
from matplotlib.image import imread
    
def list_repo(repo_path, onlyRepo=False):
    '''
    List all repositories and subrepositories from an input path (not the files)
    '''
    repo_list = []
    direc_sub_repo = [ name for name in os.listdir(repo_path) if os.path.isdir(os.path.join(repo_path, name)) ]
    if onlyRepo:
        return direc_sub_repo
    if len(direc_sub_repo) >0:
        for direc in direc_sub_repo:
            for r, d, f in os.walk(repo_path+direc):
                for file in f:
                    repo_list.append(repo_path+direc+'/'+file)
    else:
        for r, d, f in os.walk(repo_path):
            for file in f:
                repo_list.append(repo_path+file)
    repo_list.sort()
    return repo_list
 
def copy_dir(src, dst):
    '''
    Copy src directory structure to the dst path
    '''
    directories = [ name for name in os.listdir(src) if os.path.isdir(os.path.join(src, name)) ]
    for d in directories :
        os.mkdir(dst+d)
    print(dst, 'structure:')
    print(os.listdir(dst))

def get_img_name(img):
    '''
    Get the image element name from its full path
    '''
    return img.split("/")[-2] +'/'+ img.split("/")[-1][:len(img.split("/")[-1])-4]
