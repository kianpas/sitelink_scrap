from usp.tree import sitemap_tree_for_homepage
import requests
from bs4 import BeautifulSoup

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

print(getPagesFromSitemap('https://lazarinastoy.com'))

def getListUniquePages(listpagesRaw):
    listPages = []
    for page in listpagesRaw:
        if page in listPages:
            pass
        else:
            listPages.append(page)
        return listPages

#getListUniquePages(getPagesFromSitemap('https://lazarinastoy.com'))

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
                if yourDomain in link["href"] or "http" not in link["href"]:
                    pass
                else:
                    externalLinksListRaw.append([url, link["href"], link.text])
            except:
                pass
        print(count, "pages checked out of ", length_list, ".")
    return externalLinksListRaw
