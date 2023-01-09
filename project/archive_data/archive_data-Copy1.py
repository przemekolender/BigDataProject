#!/usr/bin/python3.9

import requests
from bs4 import BeautifulSoup
import wget
import os
import zipfile
from zipfile import BadZipFile

klimat = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/klimat/'
opady = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/'
synop = 'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/synop/'

def find_pages(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    quote_elements = soup.find_all('a')
    
    texts = []

    for q in quote_elements:
        if q.text[0].isdigit():
            texts.append(q.text)
    return texts

def download_files(url, name):
    sub = find_pages(url)
    subsub = []
    for i in sub:
        pages = find_pages(url + i)
        for j in range(len(pages)):
            pages[j] = i + pages[j]
        subsub += pages

    os.mkdir(name)
    os.chdir(name)
    os.mkdir('zips')
    os.mkdir('files')
    os.chdir('zips')

    for t in subsub:
        wget.download(url + t)

    os.chdir('/home/vagrant/project/archive_data')
    
    

def unzip_files(directory, destination):
    os.chdir(directory)
    files = os.listdir('.')
    for f in files:
        try:
            with zipfile.ZipFile(f, 'r') as zip_ref:
                zip_ref.extractall(destination)
        except BadZipFile:
            print(f)

def main():
    os.chdir('/home/vagrant/project/archive_data')

    download_files(klimat, 'klimat')
    download_files(opady, 'opady')
    download_files(synop, 'synop')  

    unzip_files('klimat/zips', '../files')
    os.chdir('/home/vagrant/project/archive_data')
    unzip_files('opady/zips', '../files')
    os.chdir('/home/vagrant/project/archive_data')
    unzip_files('synop/zips', '../files')

if __name__ == "__main__":
    main()
