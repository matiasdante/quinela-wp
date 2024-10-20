import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template_string

app = Flask(__name__)

# URL de la página web
URL = "https://www.jugandoonline.com.ar/"

# Provincias con los ID de los divs
provincias = [
    ('MainContent_CabezasHoyCiudadDiv', 'Ciudad'),
    ('MainContent_CabezasHoyProvBsAsDiv', 'Provincia de Buenos Aires'),
    ('MainContent_CabezasHoyMontevideoDiv', 'Montevideo'),
    ('MainContent_CabezasHoyCordobaDiv', 'Córdoba'),
    ('MainContent_CabezasHoySantaFeDiv', 'Santa Fe'),
    ('MainContent_CabezasHoyEntreRiosDiv', 'Entre Ríos'),
    ('MainContent_CabezasHoyMendozaDiv', 'Mendoza')
]

def obtener_datos_quiniela():
    response = requests.get(URL)
    resultados_quiniela = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        def extraer_resultados_provincia(id_div, nombre_provincia):
            div = soup.find(id=id_div)
            resultados = []
            if div:
                items = div.find_all('div', class_='col-xs-5')
                for item in items:
                    sorteo = item.find('a', class_='enlaces-quinielas-2021')
                    numero = item.find('a', class_='enlaces-numeros')
                    if sorteo and numero:
                        resultados.append((sorteo.text.strip(), numero.text.strip()))
                resultados_quiniela[nombre_provincia] = resultados
            else:
                resultados_quiniela[nombre_provincia] = "No se encontraron resultados"

        for id_div, nombre_provincia in provincias:
            extraer_resultados_provincia(id_div, nombre_provincia)

    return resultados_quiniela

@app.route('/')
def mostrar_resultados():
    datos = obtener_datos_quiniela()
    template = """
    <html>
    <head><title>Resultados de la Quiniela</title></head>
    <body>
        <h1>Resultados de la Quiniela</h1>
        {% for provincia, resultados in datos.items() %}
            <h2>{{ provincia }}</h2>
            {% if resultados != "No se encontraron resultados" %}
                <ul>
                {% for sorteo, numero in resultados %}
                    <li>{{ sorteo }}: {{ numero }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No se encontraron resultados para {{ provincia }}</p>
            {% endif %}
        {% endfor %}
    </body>
    </html>
    """
    return render_template_string(template, datos=datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

