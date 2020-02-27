import os
import time
import webbrowser
from shutil import move
from HtmlParser import HtmlParser
from HtmlExtractor import HtmlExtractor

def save_tokens(webpage, dir_name, dst_PATH, dwl_dir, sleep = 5, verbose = True):

    os.makedirs(dst_PATH+dir_name, exist_ok=True)

    if verbose:
        print('============================')
        print(dir_name)

    imgNameExtractor = HtmlExtractor(['\<em>','\</em>'], ['<div class='], lambda x : x[x.index('>')+1:x.index('</')] )
    urlExtractor = HtmlExtractor(['<a class="lightly" href="h'], None, lambda x : x[25:-2])
    roll20Parser = HtmlParser([urlExtractor, imgNameExtractor])
    urlAndNames = roll20Parser.parse(webpage)
    links = urlAndNames[urlExtractor]
    names = urlAndNames[imgNameExtractor]

    assert(len(links) == len(names))

    if verbose:
        print('============================')
        print('Found', len(links), 'extracted images')
        print('============================')

    for j in range(len(links)):
        url = links[j]
        webbrowser.get('windows-default').open_new_tab(url)
        time.sleep(sleep)
        _name = names[j]
        if verbose:
            print(j, '--', _name, '--', url)     
        for _img in os.listdir(dwl_dir):
            if (str(_img)[:3] == 'max') and (str(_img)[-1] == 'g'):
                move(dwl_dir+_img, dst_PATH +dir_name+'/'+_name+'.png')

    if not (len(os.listdir(dst_PATH +dir_name)) == len(links)):
        print('WARNING: number of url different than final number of images')