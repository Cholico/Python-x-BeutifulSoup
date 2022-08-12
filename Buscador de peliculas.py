from bs4 import BeautifulSoup
import requests

def Script(pelicula, links):
    for link in links:
        try:  # "testea el codigo de abajo, si algo sale mal, ir al bloque 'except'"
            if pelicula.find(link) != -1:
                resultado = requests.get(f'{link}')  # estructura --> https://subslikescript.com/movie/X-Men_2-290334
                contenido = resultado.text
                soup = BeautifulSoup(contenido, 'lxml')

                # Localizar la caja (box) que contiene cada titulo (title) y transcript
                box = soup.find('article', class_='main-article')
                # Localizar el titulo (title) y transcript
                title = box.find('h1').get_text()
                transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

                # Exportar la data en un archivo .txt con el nombre/titulo de la pelicula
                with open(f'{title}.txt', 'w') as file:
                    file.write(transcript)
        except:
            print('------ Link not working -------')  # Mensaje en caso el link no funcione
            print(link)



def Busqueda(enlaces):

    box = enlaces.find('article', class_='main-article')
    links = []

    for link in box.find_all('a', href=True):  # find_all genera una lista
        links.append(link['href'])

    pelicula = input('Dame el nombre de una pelicula a buscar: ')


    Script(pelicula.replace(' ', '_'), links)


def paginacion(raiz, soup):

    pagination = soup.find('ul', class_='pagination')
    paginas = pagination.findAll('li', class_='page-item')
    last_page = paginas[-2].text

    for pagina in range(1, int(last_page)+1):
        resultado = requests.get(f'{raiz}?page={pagina}')
        contenido = resultado.text
        enlaces = BeautifulSoup(contenido, 'lxml')

    Busqueda(enlaces)



def obtnerPagina():

    raiz = 'https://subslikescript.com/movies'
    resultado = requests.get(raiz)
    contenido = resultado.text
    soup = BeautifulSoup(contenido, 'lxml')

    paginacion(raiz, soup)

obtnerPagina()