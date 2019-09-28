from pd import  pandas
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from tqdm import  tqdm

ii = 1
repository = []
projects_name = []
mylink = []
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
                mylink.append(tag)
            print(f'{projects_name[i]}===>', tag)
        except:
            print("error")


def download(url, file_name):
    # get_response = requests.get(url, stream=True)
    file_name = url.split("/")[-3] + ".zip"
    r = requests.get(url, stream=True)
    # Total size in bytes.
    total_size = int(r.headers.get('content-length', 0))
    block_size = 1024  # 1 Kibibyte
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    print(f'{file_name}===========>')
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(block_size):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                t.update(len(chunk))


# def download(url, file_name):
#     get_response = requests.get(url, stream=True)
#     file_name = url.split("/")[-3] + ".zip"
#     with open(file_name, 'wb') as f:
#         for chunk in get_response.iter_content(chunk_size=1024):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)


def downloadlink():
    for url in range(len(mylink)):
        download(mylink[url], projects_name[url])


def setrepository(url):
    if len(url) > 2:
        repository.clear()
        repository.append(url)
        recusiveappend(url)
    else:
        print("empty")
    getrepository()


def recursejump(url):
    print(url)


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


# recusiveappend('https://github.com/iampawan?tab=repositories')
# for a in repository:
#     print(a)
setrepository('https://github.com/kaina404?tab=repositories')
getdwonloadlink()
downloadlink()
