from usp.tree import sitemap_tree_for_homepage
import requests
from bs4 import BeautifulSoup
import pandas as pd


# tree = sitemap_tree_for_homepage('https://lazarinastoy.com')
# # print(tree)
# for page in tree.all_pages():
#     print(page.url)


def getPagesFromSitemap(fullDomain):
    listPagesRaw = []
    tree = sitemap_tree_for_homepage(fullDomain)
    for page in tree.all_pages():
        listPagesRaw.append(page.url)
    return listPagesRaw

#print(getPagesFromSitemap('https://lazarinastoy.com'))

def getListUniquePages(listpagesRaw):
    listPages = []
    for page in listpagesRaw:
        if page in listPages:
            pass
        else:
            listPages.append(page)
        return listPages

#print(getListUniquePages(getPagesFromSitemap('https://lazarinastoy.com')))

def ExternalLinkList(listPages):
    externalLinksListRaw = []
    count = 0
    length_list = len(listPages)
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
    for url in listPages:
        count = count + 1
        request = requests.get(url, headers=user_agent)
        content = request.content
        soup = BeautifulSoup(content, 'lxml')
        list_of_links = soup.find_all("a")
        for link in list_of_links:
            try:
                if 'https://lazarinastoy.com' in link["href"] or "http" not in link["href"]:
                    pass
                else:
                    externalLinksListRaw.append([url, link["href"], link.text])
            except:
                pass
        print(count, "pages checked out of", length_list,".")
    return externalLinksListRaw

print(">>>>",ExternalLinkList(getListUniquePages(getPagesFromSitemap('https://lazarinastoy.com'))))

def getUniqueExternalLinks(externalLinksListRaw):
    uniqueExternalLinks = []
    for link in externalLinksListRaw:
        if link[1] in uniqueExternalLinks:
            pass
        else:
            uniqueExternalLinks.append(link[1])
    return uniqueExternalLinks

print(">>>>>>>", getUniqueExternalLinks(ExternalLinkList(getListUniquePages(getPagesFromSitemap('https://lazarinastoy.com')))))

def identifyBrokenLinks(uniqueExternalLinks):
    count = 0
    length_uniqueExternalLinks = len(uniqueExternalLinks)
    user_agent = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
    brokenLinksList = []

    for link in uniqueExternalLinks:
        count = count + 1
        print("Checking external link #",count, "out of", length_uniqueExternalLinks,".")
        try:
            statusCode = requests.get(link, headers=user_agent).status_code
            if statusCode == 404:
                brokenLinksList.append(link)
            else:
                pass
        except:
            brokenLinksList.append(link)
    return brokenLinksList


print(">>>>>>>>>",identifyBrokenLinks(getUniqueExternalLinks(ExternalLinkList(getListUniquePages(getPagesFromSitemap('https://lazarinastoy.com'))))))


def matchBrokenLinks(brokenLinksList, externalLinksListRaw):
    brokenLinkLocation = []
    for link in externalLinksListRaw:
        if link[1] in brokenLinksList:
            brokenLinkLocation.append([link[0], link[1], link[2]])
        else:
            pass

    dataframeFinal = pd.DataFrame(brokenLinkLocation, columns=["URL", "Broken Link URL", "Anchor Text"])
    return dataframeFinal