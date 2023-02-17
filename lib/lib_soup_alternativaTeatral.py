from webbrowser import get
from lib.lib_soup import *


#REVISAR
def url_getInt(url):
    return url.replace('https://www.alternativateatral.com','')

def int_getUrl(cod):
    return 'https://www.alternativateatral.com/'+cod


def obra_getTitulo(soup):
    title       = soup.find("meta", {"name":"title"})["content"]
    return title

def int_getTitulo(cod):
    url = int_getUrl(cod)
    soup = url_to_soup(url)
    return obra_getTitulo(soup)


def obra_getFichaTecnica(soup):
    ficha = soup.find("div", {"class":"alter-padding-left alter-padding-right alter-padding-bottom content-fichatecnica"})   
    ficha = ficha.find("dl")
    ficha = ficha.find_all("a")
    return ficha

def obra_getPersonas_int(soup):
    #Devuelve el int de todas las personas en una obra.
    ficha = obra_getFichaTecnica(soup)
    x = []
    for i in ficha:
        if 'asp?c=' not in str(i):
            x.append(i['href'])
    return x

def obra_getPersonas(soup):
    try:
        #Devuelve (rubro, nombre, url) de todas las personas en una obra
        ficha = obra_getFichaTecnica(soup)
        x = []
        for i in ficha:
            if 'asp?c=' in str(i):
                rubro = i.text
            else:
                x.append((rubro,i.text,int_getUrl(i['href'])))
        return x
    except: return []

def obra_getTeatros(soup):
    try:
        soup = soup.find("section", {"class":"section_vinculos alter-padding-left alter-padding-right"})
        urls = get_links(soup)
    except: urls = []
    return urls 


def obra_info(url):
    soup = url_to_soup(url)
    (title,soup) = soup.html.body.findChild("div",{"class":"mdc-drawer-app-content"}).findChildren("div", {"class":"row"})

    title = title.text

    people = obra_getPersonas(soup)
    
    return title, url, people

def obra_info2(url):
    soup = url_to_soup(url)
    people  = obra_getPersonas(soup)
    teatros = obra_getTeatros(soup)    
    return (url, people, teatros)

def persona_getObras_int(soup):
    y = soup.find("ul", {"id":"listado-trayectoria"})
    y = get_links(y)
    return y






def buscarObra(titulo):
    url = "https://www.alternativateatral.com/buscar.asp?texto="+titulo.replace(" ","%20")+"&objetivo=Obras"
    soup = url_to_soup(url)
    #UBICO LA SECCIÓN EN DONDE BUSCAR LOS links
    try:
        soup = soup.find("body")
        soup = soup.find("div",{"class":"mdc-drawer-app-content"})
        soup = soup.find("div",{"class":"row mdc-top-app-bar--fixed-adjust"})
        soup = soup.find("div",{"class":"main"})
        soup = soup.find("div",{"class":"alter-padding"})
        soup = soup.find("div",{"class":"resultados"})
        links = get_links(soup)
        return links
    except:
        return []



#REVISARÍA LAS FUNCIONES DE OPINIONES.


def opiniones_url_i(i, url='https://www.alternativateatral.com/opinion_publico.php?pagina='):
    return url+str(i)

def opiniones_getOpiniones(i,url='https://www.alternativateatral.com/opinion_publico.php?pagina='):
    url = opiniones_url_i(i,url)
    soup = url_to_soup(url)
    soup = soup.find("body")
    soup = soup.find("div",{"class":"mdc-drawer-app-content"})
    soup = soup.find("div",{"class":"row mdc-top-app-bar--fixed-adjust"})
    soup = soup.find("div",{"class":"main"})
    soup = soup.find("div",{"class":"alter-padding content-opiniones"})
    soup = soup.find("ul",{"class":"opiniones"})
    L    = soup.find_all("li",{"class":"opinion-general"})
    L    = [(get_links(s)[0],  s.find("span",{"class":"calificacion"})["content"]) for s in L]
    L    = [(l[0].replace('//www.alternativateatral.com/opiniones','https://www.alternativateatral.com//obra'),l[1]) for l in L]
    return L 


def opinionesObra_pagMax(url):
    try:
        soup = url_to_soup(url+'1')
        soup = soup.find("body")
        soup = soup.find("div",{"class":"mdc-drawer-app-content"})
        soup = soup.find("div",{"class":"row mdc-top-app-bar--fixed-adjust"})
        soup = soup.find("div",{"class":"main"})
        soup = soup.find("div",{"class":"alter-padding content-opiniones"})
        soup = soup.find("nav")
        soup = soup.find("ul")
        t    = soup.find_all("li",{"class":"page-item"})[-2].text
        return int(t)
    except: return 1

def opinionesObra_getOpiniones(url,max):
    users = []
    for i in range(1,max+1):
        soup = url_to_soup(url+str(i))      
        soup = soup.find("div",{"class":"mdc-drawer-app-content"})
        soup = soup.find("div",{"class":"row mdc-top-app-bar--fixed-adjust"})
        soup = soup.find("div",{"class":"main"})
        soup = soup.find("div",{"class":"alter-padding content-opiniones"})
        soup = soup.find("ul",{"class":"opiniones"})
        L    = soup.find_all("li",{"class":"opinion-general"})
        L    = [l.find_all("span",{"class":"autor"})[1] for l in L]
        for l in L:
            try: 
                if int(l.find("span", {"class":"badgeopinion badge-opinador"}).text)>=25:
                            users += [get_links(l)]
            except:
                None

    return users