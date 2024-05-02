import os
from bs4 import BeautifulSoup
from qmenzi import config

CACHE_FOLDER = config('global.cache_folder')

def html2txt(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')    
    return soup.get_text()


def write_content_to_file(content_id, content):
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    file = f'{CACHE_FOLDER}/{content_id}.txt'
    with open(file, 'w') as f:
        for line in content:
            f.write(f'{line}\n')


def read_content_from_file(content_id, default=''):
    file = f'{CACHE_FOLDER}/{content_id}.txt'
    if os.path.exists(file):
        with open(file, 'r') as f: 
            return f.readlines()
    else:
        return default

