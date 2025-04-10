import bs4
import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import colorama
import re

colorama.init(autoreset=True)

visitedPaths = set()
logFileHandle = None

def IsValidUrl(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def UrlPathDictionary(url):
    """Converts a url from: http://www.test.com/folder/file.txt to: http://www.test.com/folder/"""
    return re.sub(r'\.\w+$', '', url)

def IsSubPath(url, base_url):
    if not url.startswith(base_url):
        print(colorama.Back.MAGENTA + "[NOT SUBPATH]:" + colorama.Style.RESET_ALL +
              colorama.Fore.MAGENTA + " " + url)
        return False
    return True
    
def GetEveryWebsiteSubPath(url, base_url, maxDepthOption=False, onlySubPaths=False, depth=0, maxDepth=5):
    if depth > maxDepth:
        print(colorama.Fore.YELLOW + f"Max depth reached at: {url}")
        return

    print(colorama.Fore.CYAN + colorama.Style.BRIGHT + f"Processing URL: {url}")
    try:
        res = req.get(url)
        res.raise_for_status()
    except Exception as e:
        print(colorama.Back.RED + "[ERROR]:" + colorama.Style.RESET_ALL +
              colorama.Fore.RED + f" Error fetching {url}: {e}")
        return

    try:
        soup = BeautifulSoup(res.text, 'html.parser')
        for tag in soup.find_all('a', href=True):
            subpath = tag.get('href')
            if subpath.startswith("/"):
                full_url = urljoin(url, subpath)
                if full_url not in visitedPaths:
                    if onlySubPaths and not IsSubPath(full_url, base_url):
                        continue
                    
                    print(colorama.Back.GREEN + "[NEW URL]:" + colorama.Style.RESET_ALL +
                          colorama.Fore.GREEN + " " + full_url)
                    visitedPaths.add(full_url)

                    if logFileHandle is not None:
                        logFileHandle.write(full_url + "\n")
                        logFileHandle.flush()
                    
                    GetEveryWebsiteSubPath(url=full_url, base_url=base_url,
                                           onlySubPaths=onlySubPaths, depth=depth+1 if maxDepthOption else depth, maxDepth=maxDepth)
    
    except bs4.exceptions.ParserRejectedMarkup as e:
        print(colorama.Back.RED + "[ERROR]:" + colorama.Style.RESET_ALL +
              colorama.Fore.RED + f" Error parsing {url}: {e}")

def UI():
    global logFileHandle
    print(""" ____  _   _ ____        ____   _  _____ _   _ 
/ ___|| | | | __ )      |  _ \ / \|_   _| | | |
\___ \| | | |  _ \ _____| |_) / _ \ | | | |_| |
 ___) | |_| | |_) |_____|  __/ ___ \| | |  _  |
|____/ \___/|____/___  _|_|_/_/__ \_\_| |_| |_|
|  ___|_ _| \ | |  _ \| ____|  _ \             
| |_   | ||  \| | | | |  _| | |_) |            
|  _|  | || |\  | |_| | |___|  _ <             
|_|   |___|_| \_|____/|_____|_| \_\            """)

    print("Made by William Jacobsen - 2025\n")
    print("This tool will help find a path of a website,\nwithout using the traditional bruteforce (fuzzing) method.\nInstead we find every href attribute and use recursive depth-first search to web crawl the urls...\n")

    url = ""
    while not IsValidUrl(url):
        url = input("URL: ")

    base_url = UrlPathDictionary(url)
    
    onlySubPaths = input("Only search sub-paths? (Default: 0) (0 or 1): ")
    if onlySubPaths == "":
        onlySubPaths = False
    else:
        onlySubPaths = bool(int(onlySubPaths))
    
    maxDepth = input("Max Depth (Default: no max depth): ")
    if maxDepth == "":
        maxDepth = 0
        maxDepthOption = False
    else:
        maxDepth = int(maxDepth)
        maxDepthOption = True
    
    logFile = input("Save urls in filename.txt (leave empty to skip): ")
    if logFile.strip() != "":
        logFileHandle = open(logFile, "w")
    
    GetEveryWebsiteSubPath(url=url, base_url=base_url, maxDepthOption=maxDepthOption, onlySubPaths=onlySubPaths, maxDepth=maxDepth)
    
    if logFileHandle is not None:
        logFileHandle.close()
    
    print(colorama.Fore.YELLOW + "Crawling complete. URLs have been logged.")

if __name__ == '__main__':
    import os
    os.system('cls')
    UI()
