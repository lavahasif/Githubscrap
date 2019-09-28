# repository download based on language wise
import time

import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.request import urlopen

ii = 1
limit = 0
repository = []
projects_name = []
mylink = []
projects = []
downloadlink = []
githublink = 'https://github.com'

repository.append('https://github.com/lavahasif?tab=repositories')


def getinformation(list):
    try:
        for count in range(len(list)):
            print(f'{count}=======>', list[count])

    except:
        print('some problem')


def getinformation1(link):
    print(link)


def getnextlink(rep, x=0):
    linkss = ''
    # x = 0
    html = urlopen(rep).read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    if len(projects) >= 10:
        time.sleep(1)
    try:
        for a in soup.find_all('div', attrs={'class': 'paginate-container'}):
            linkss = githublink + (a.find('a', attrs={'rel': 'next'})).attrs['href']
        getinformation1(linkss)
        while (len(projects) < 10 + x):
            getrepository(linkss)
        getdwonloadlink(linkss)
    except Exception as e:
        print(e)


def getrepository(rep, x):
    # for rep in repository:
    print(rep)
    html = urlopen(rep).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    for a in soup.find_all('li', attrs={'class': 'repo-list-item'}):
        tag = a.find('a', attrs={'class': 'v-align-middle'})
        link = tag.attrs['href']
        projects_name.append(tag.text)
        # print(tag.text, githublink + link)
        projects.append(githublink + link)

    getinformation(projects)
    getnextlink(rep, x)


def getdwonloadlink(linkss):
    for i in range(len(projects)):
        try:
            html = urlopen(projects[i]).read().decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')

            for a in soup.find_all('a', attrs={'class': 'btn'}, string='Download ZIP'):
                # tag = githublink + (a.find('a', attrs={'class': 'btn'})).attrs['href']
                tag = githublink + a.attrs['href']
                mylink.append(tag)
            # print(f'{projects_name[i]}===>', tag)


        except Exception as e:
            print(e)
    getinformation(mylink)
    while (len(mylink) < limit):
        getrepository(linkss, 10)


def download(url, file_name, count):
    # get_response = requests.get(url, stream=True)
    file_name = url.split("/")[-3] + ".zip"
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    mysize=0
    t = tqdm(total=total_size, unit='B', unit_scale=True)
    print(f'{count}--{file_name}===========>\n')
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(block_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                mysize=mysize+len(chunk)
        t.update(mysize)


def downloadlink():
    for url in range(len(mylink)):
        download(mylink[url], projects_name[url], url)


def setrepository(url):
    if len(url) > 2:
        repository.clear()
        repository.append(url)
        # recusiveappend(url)
    else:
        print("empty")
    getrepository(url, 0)


def recusiveappend(url):
    # print(url)
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, features='lxml')
    for a in soup.findAll('div', attrs={'class': 'BtnGroup'}):
        try:
            tag = a.find('a', attrs={'class': 'btn'}, string='Next').attrs['href']
            name = a.find('a', attrs={'class': 'btn'}).text
            if len(tag) > 3:
                # print(tag)
                if 'after' in tag:
                    repository.append(tag)
                    recusiveappend(tag)

        except:
            print("error")


limit = 10
# recusiveappend('https://github.com/iampawan?tab=repositories')
# for a in repository:
#     print(a)
# setrepository('')

# setrepository('https://github.com/search?utf8=%E2%9C%93&q=rx+java&type=')
setrepository('https://github.com/search?utf8=%E2%9C%93&q=rx+java&type=')
# getdwonloadlink()
downloadlink()
