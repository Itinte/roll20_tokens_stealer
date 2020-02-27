import os
import argparse
from urllib.request import Request, urlopen
from roll20_scrapper import save_tokens
'''
# EXAMPLE OF CMD CALL ##
python scrap_url_cmd.py --url https://marketplace.roll20.net/browse/set/4549/infernal-war-token-set-2
'''

''' 
CONFIG
''' 
DOWNLOAD_FOLDER = '**PATH_DOWNLOAD_FOLDER**'
DEFAULT_OUTPUT_DIRECTORY = '/scrapping_results/'

parser = argparse.ArgumentParser(description='Save images from ROLL20 webpage url')
parser.add_argument('--url', type = str, help='Webpage url from which we download the available images')
parser.add_argument('--o', type = str, help='Name of the folder where we save the downloaded images; By default, will get the url last part')
parser.add_argument('--v', type = bool, default = True,  help='Print process steps')
parser.add_argument('--s', type = float, default = 2,  help='Sleeping time between each scrap')

def main():
    
    args = parser.parse_args() # Parse script arguments
    if args.url is None:
        raise Exception('No url has been given')

    script_directory = os.path.dirname(os.path.abspath(__file__))

    if args.o is None :
        args.o = args.url.split('/')[-1]

    OUT = script_directory + DEFAULT_OUTPUT_DIRECTORY
    os.makedirs(OUT, exist_ok=True)

    req = Request(args.url, headers={'User-Agent': 'Mozilla/5.0'})
    page = str(urlopen(req).read()).replace('\\t', '').split('\\n')
    save_tokens(page, args.o, OUT, DOWNLOAD_FOLDER, args.s, args.v)

if __name__ == "__main__":
    main()