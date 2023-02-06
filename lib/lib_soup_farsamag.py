from msilib.schema import Error
from lib.lib_soup import *
import unicodedata 

def obra_getTitulo(soup):
#BUSCO TÍTULO
    try:
        soup = soup.find("head")
        soup = soup.find("title")
    #APLICO FORMATO    
        title = soup.text
        title = title.replace(" - Farsa Mag","")
        return title
    except:
        return "ERROR - PROBLEMA AL BUSCAR TÍTULO"

#INCOMPLETO
def obra_getPersonas(soup):
    try:
#BUSCO FICHA
        soup = soup.find("body")
        soup = soup.find("div", {"id":"page"})
        soup = soup.find("main", {"id":"site-content"})
        soup = soup.find("section",{"class":"with-sidebar container"})
        soup = soup.find("div",{"class":"articles"})
        soup = soup.find("article")
        soup = soup.find("div",{"class":"article-content"})
        soup = soup.find("section",{"class":"section section-ficha"})
        if soup == None:
            return []
    #UBICO PERSONAS
        personas = soup.find_all("p")
    #APLICO FORMATO
        personas = [x.text for x in personas]
        personas = [x.split(":") for x in personas if ":" in x]
        personas = [[x[0],unicodedata.normalize("NFKD", x[1])] for x in personas]
        personas = [[x[0],x[1].split(",")] for x in personas]
        Z=[]
        for persona in personas:
            Y = [[persona[0],y] for y in persona[1]]
            Z += Y
        personas = Z
        return personas
    except:
        return []

        
def obra_getBadges(soup):
    titulo = obra_getTitulo(soup)
    try:
        soup = soup.find("body")
        soup = soup.find("div", {"id":"page"})
        soup = soup.find("main", {"id":"site-content"})
        soup = soup.find("section",{"class":"single-cartelera container"})
        soup = soup.find("div", {"class":"badges"})
        return soup
    except:
        print("ERROR - ", titulo, " NO HAY div badges")
        return ValueError

#INCOMPLETO
def obra_getDuracion(soup):
    titulo = obra_getTitulo(soup)
    soup = obra_getBadges(soup)
    try:
        soup = soup.find("div",{"class":"badge badge-duracion"})
        text = soup.text
        return text
    except:
        print("ERROR -", titulo, "NO INCLUYE DURACION")
        return ValueError


def obra_getCategoria(soup):
    titulo = obra_getTitulo(soup)
    soup = obra_getBadges(soup)
    text = soup.text
    if "Imperdible" in text:
        return "Imperdible"
    if "Destacada" in text:
        return "Destacada"
    if "Reseña" in text:
        return "Reseña" 
    print("ERROR -", titulo, "NO INCLUYE CATEGORÍA")
    return ValueError
    


def archivo_getUrls():
    soup = url_to_soup("https://farsamag.com/archivo-de-obras/")
    soup = soup.find("body")
    soup = soup.find("div",{"id":"page"})
    soup = soup.find("main",{"id":"site-content"})
    soup = soup.find("section",{"class":"section section-cartelera container"})
    soup = soup.find("div",{"class":"section-list row"})
    X = soup.find_all("a")
    X = [x["href"] for x in X]
    return list(set(X))

def cartelera_getUrls():
    soup = url_to_soup("https://farsamag.com/cartelera/")
    soup = soup.find("body")
    soup = soup.find("div",{"id":"page"})
    X = soup.find_all("a")
    X = [x["href"] for x in X]
    X = [x for x in X if "farsamag.com/obras/" in x]
    return list(set(X))

def Obras_getUrls():
    X =  cartelera_getUrls()
    X += archivo_getUrls()
    return list(set(X))

