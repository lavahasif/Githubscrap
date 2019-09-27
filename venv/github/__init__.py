# only for learning purpose

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

repository = []
projects_name = []
projects = []
downloadlink = []
githublink = 'https://github.com'

repository.append('https://github.com/lavahasif?tab=repositories')


def getrepository():
    for rep in repository:
        print(rep)
        html = urlopen(rep).read().decode('utf-8')
        soup = BeautifulSoup(html, features='lxml')
        for a in soup.findAll('div', attrs={'class': 'd-inline-block mb-1'}):
            tag = a.find('a')
            link = tag.attrs['href']
            projects_name.append(tag.text)
            # print(tag.text, githublink + link)
            projects.append(githublink + link)


def getdwonloadlink():
    for i in range(len(projects)):
        try:
            html = urlopen(projects[i]).read().decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')

            for a in soup.findAll('div', attrs={'class': 'mt-2'}):
                tag = githublink + a.find('a', attrs={'class': 'btn'}).attrs['href']
            print(f'{projects_name[i]}===>', tag)
        except:
            print("error")


getrepository()
getdwonloadlink()
