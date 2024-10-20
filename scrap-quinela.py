import requests
from bs4 import BeautifulSoup

url = 'https://www.jugandoonline.com.ar/'

response = requests.get(url)

provincias = [
    ('MainContent_CabezasHoyCiudadDiv', 'Ciudad'),
    ('MainContent_CabezasHoyProvBsAsDiv', 'Provincia de Buenos Aires'),
    ('MainContent_CabezasHoyCordobaDiv', 'Córdoba'),
    ('MainContent_CabezasHoySantaFeDiv', 'Santa Fe'),
    ('MainContent_CabezasHoyEntreRiosDiv', 'Entre Ríos'),
    ('MainContent_CabezasHoyMendozaDiv', 'Mendoza')
]

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    def extraer_resultados_provincia(id_div, nombre_provincia):
        div = soup.find(id=id_div)
        if div:
            resultados = div.find_all('div', class_='col-xs-5')
            print(f"\nResultados Quiniela {nombre_provincia}:")
            for resultado in resultados:
                sorteo = resultado.find('a', class_='enlaces-quinielas-2021')
                numero = resultado.find('a', class_='enlaces-numeros')
                if sorteo and numero:
                    print(f"{sorteo.text.strip()}: {numero.text.strip()}")
        else:
            print(f"No se encontraron resultados para {nombre_provincia}.")

    for id_div, nombre_provincia in provincias:
        extraer_resultados_provincia(id_div, nombre_provincia)

else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")



