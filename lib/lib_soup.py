from bs4 import BeautifulSoup
import requests



def url_to_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    return soup

def soup_to_text(soup):
    y = ''
    for x in soup.strings:
        y += '  ' + x
    y.replace(u'\n', u'.  ')
    y = ' '.join( y.split() )
    y = y.upper()
    return y


def get_links(soup):    
  links = []
  for link in soup.find_all('a'):
    if link.has_attr('href'):
      links.append(link["href"])
  return links
