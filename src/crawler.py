from googlesearch import search
import requests
from bs4 import BeautifulSoup
from constants import NUMBER_OF_GOOGLE_WEBPAGES_TO_BE_SEARCHED

def get_first_n_google_webpages_for_searched_string(string=None, n=NUMBER_OF_GOOGLE_WEBPAGES_TO_BE_SEARCHED):
    urls = []
    for url in search(string, stop=n):
        urls.append(url)
    return urls

def get_responce_text_paragraphs(url):
    print("Check %s " % url)
    responce = requests.get(url)
    content = responce.content
    soup = BeautifulSoup(content, 'html.parser')
    paragraphs = []
    for data in soup.find_all("p"):
        paragraphs.append(data.get_text())
    return paragraphs

if __name__ == "__main__":
    string = "френска революция"
    urls = get_first_n_google_webpages_for_searched_string(string, n=1)
    for url in urls:
        get_responce_text_paragraphs(url)
        break