<h1 align="center">
  Quiniela Sarco
  <br>
  <a href="https://github.com/matiasdante">
    <img src="https://www.loteria.gba.gov.ar/images/logos/01_LogoQuinielaMultiple.png" alt="Quiniela Sarco" width="200">
  </a>
</h1>

<h4 align="center">Sistema Avanzado de Análisis de Datos para Quiniela - Predicciones Inteligentes y Dashboard Interactivo</h4>

<p align="center">
  <a href="#características">Características</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#uso">Uso</a> •
  <a href="#api">API</a> •
  <a href="#docker">Docker</a> •
  <a href="#créditos">Créditos</a>
</p>

Este proyecto ha sido reestructurado para separar la API del frontend, permitiendo mayor escalabilidad y mantenimiento.

## Estructura del Proyecto

```
quinela-wp/
├── api/                    # Servidor API (Flask)
│   ├── backend/           # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── api.py
│   │   ├── database.py
│   │   └── scraper.py
│   ├── config.py          # Configuración
│   ├── main_api.py        # Punto de entrada de la API
│   └── requirements.txt   # Dependencias Python
├── frontend/              # Aplicación web estática
│   ├── index.html         # Página principal
│   ├── styles.css         # Estilos
│   └── script.js          # Lógica del frontend
├── nginx.conf             # Configuración de Nginx
└── README.md
```


## Características

### 🎯 Análisis Avanzado

- **Análisis Estadístico**: Análisis de frecuencia de números por mes, semana y períodos personalizados
- **Números Hot/Cold**: Detección inteligente de números en tendencia y números raros
- **Reconocimiento de Patrones**: Patrones semanales y detección de números consecutivos
- **Recomendaciones Inteligentes**: Predicciones potenciadas por IA basadas en datos históricos

### 📊 Dashboard Moderno

- **Diseño Responsivo**: Interfaz hermosa y adaptable a dispositivos móviles
- **Datos en Tiempo Real**: Resultados de lotería en vivo de múltiples provincias
- **Visualizaciones Interactivas**: Tarjetas de estadísticas y gráficos de frecuencia
- **Soporte Multi-provincia**: Análisis de todas las provincias argentinas

### 🔄 Recolección Automatizada de Datos

- **Scraping Automático**: Recolección de datos programada cada hora
- **Almacenamiento Histórico**: Base de datos SQLite para análisis de datos a largo plazo
- **Manejo de Errores**: Gestión robusta de errores y logging
- **Validación de Datos**: Resultados de lotería limpios y validados

### 🚀 Arquitectura API-First

- **API RESTful**: API completa para toda la funcionalidad
- **Respuestas JSON**: Datos estructurados para fácil integración
- **Análisis en Tiempo Real**: Cálculos estadísticos en vivo
- **Extensible**: Fácil de agregar nuevas características de análisis

## Instalación y Configuración

### 1. Configurar el Servidor API

```bash
cd api
pip install -r requirements.txt
```

### 2. Iniciar el Servidor API

```bash
cd api
python main_api.py
```

La API estará disponible en `http://localhost:5000`

### 3. Configurar Nginx

1. Copia los archivos del frontend a `/var/www/quinela-frontend/`
2. Copia `nginx.conf` a tu directorio de configuración de Nginx
3. Reinicia Nginx

### 4. Acceder a la Aplicación

- Frontend: servido por Nginx según `nginx.conf` (ej. `http://localhost`)
- API directa: `http://localhost:5000/api/`

## Endpoints de la API

### Datos Principales

- `GET /api/health` - Estado de salud del servicio
- `GET /api/current` - Resultados actuales de la quiniela
- `GET /api/provinces` - Lista de provincias disponibles

### Análisis y Estadísticas

- `GET /api/analytics/monthly` - Análisis de frecuencia mensual
- `GET /api/analytics/hot-cold?days=30` - Números calientes y fríos
- `GET /api/analytics/patterns` - Patrones detectados
- `GET /api/recommendations` - Recomendaciones inteligentes
- `GET /api/stats` - Estadísticas generales

### Datos Históricos

- `GET /api/history?days=30&provincia=Buenos+Aires` - Datos históricos
- `GET /api/frequency?days=30&numero=15` - Análisis de frecuencia

### Gestión de Datos

- `POST /api/scrape` - Ejecutar scraping manual

## Instalación

### Requisitos Previos

### Inicio Rápido

1. **Clonar el repositorio**:

```bash
git clone https://github.com/matiasdante/quinela-wp.git
cd quinela-wp
```

```bash
cp .env.example .env
# Editar .env con tus configuraciones preferidas
```

4. **Ejecutar la aplicación**:

```bash
python main.py
```

5. **Acceder al dashboard**:

   Abrir [http://localhost:5000](http://localhost:5000) en tu navegador

## Uso

### Dashboard Web

El dashboard principal proporciona:

- Resultados actuales de lotería de todas las provincias
- Análisis de frecuencia mensual
- Recomendaciones inteligentes de números
- Acceso rápido a endpoints de la API

### Recolección Manual de Datos

Activar scraping manual:

```bash
curl -X POST http://localhost:5000/api/scrape
```

### Consultas de Análisis

Obtener análisis para provincias específicas:

```bash
# Análisis mensual para Buenos Aires
curl "http://localhost:5000/api/analytics/monthly?provincia=Provincia de Buenos Aires"

# Números hot/cold para los últimos 60 días
curl "http://localhost:5000/api/analytics/hot-cold?days=60"

# Recomendaciones inteligentes
curl "http://localhost:5000/api/recommendations"
```

## Desarrollo

### Estructura de Respuestas API

Todas las respuestas siguen este formato:

```json
{
  "success": true|false,
  "data": {...},
  "timestamp": "2024-01-01T12:00:00",
  "error": "mensaje de error" // solo si success: false
}
```

### Personalización

1. **API**: Modifica `api/config.py` para cambiar configuraciones
2. **Frontend**: Edita `frontend/script.js` para cambiar la URL de la API
3. **Nginx**: Ajusta `nginx.conf` según tu entorno

## Producción

### Consideraciones de Seguridad

- Configurar HTTPS con certificados SSL/TLS
- Implementar rate limiting
- Validar y sanitizar todas las entradas
- Configurar firewall apropiado

### Performance

- Usar un reverse proxy como Nginx (incluido)
- Implementar cache de Redis para datos frecuentes
- Optimizar consultas de base de datos
- Monitorear logs y métricas

### Monitoreo

- Logs de Nginx en `/var/log/nginx/`
- Logs de la aplicación según configuración
- Métricas de performance disponibles en `/api/stats`

- Validar y sanitizar todas las entradas
- Configurar firewall apropiado

### Performance

- Usar un reverse proxy como Nginx (incluido)
- Implementar cache de Redis para datos frecuentes
- Optimizar consultas de base de datos
- Monitorear logs y métricas

### Monitoreo

- Logs de Nginx en `/var/log/nginx/`
- Logs de la aplicación según configuración
- Métricas de performance disponibles en `/api/stats`

### Endpoints

| Endpoint                           | Método | Descripción                             |
| ---------------------------------- | ------- | ---------------------------------------- |
| `/`                              | GET     | Dashboard principal                      |
| `/api/current`                   | GET     | Resultados actuales de lotería          |
| `/api/scrape`                    | POST    | Activador de scraping manual             |
| `/api/analytics/monthly`         | GET     | Análisis de frecuencia mensual          |
| `/api/analytics/hot-cold`        | GET     | Números hot y cold                      |
| `/api/analytics/weekly-patterns` | GET     | Análisis de patrones semanales          |
| `/api/recommendations`           | GET     | Recomendaciones inteligentes de números |
| `/api/patterns`                  | GET     | Patrones detectados y alertas            |
| `/api/stats`                     | GET     | Estadísticas de base de datos           |
| `/api/provinces`                 | GET     | Provincias disponibles                   |

### Parámetros de Consulta

- `provincia`: Filtrar por provincia específica
- `days`: Número de días para análisis (predeterminado: 30)
- `weeks`: Número de semanas para análisis (predeterminado: 8)
- `start_date`: Fecha de inicio para consultas históricas (YYYY-MM-DD)
- `end_date`: Fecha de fin para consultas históricas (YYYY-MM-DD)

### Ejemplo de Respuesta

```json
{
  "success": true,
  "data": {
    "month": "2025-07",
    "provincia": "Ciudad",
    "total_draws": 150,
    "most_frequent": [
      {
        "numero": "1234",
        "frequency": 8,
        "percentage": 5.33
      }
    ],
    "statistics": {
      "total_unique_numbers": 120,
      "avg_frequency": 1.25,
      "median_frequency": 1,
      "max_frequency": 8,
    ## Desarrollo
    }
  }
}
```

## Troubleshooting

### Problemas Comunes

1. **API no responde**: Verificar que el servidor Flask esté ejecutándose
2. **CORS errors**: Verificar configuración de Nginx y Flask-CORS
3. **Frontend no carga datos**: Verificar que la URL de la API sea correcta
4. **Permisos de archivos**: Asegurar que Nginx pueda leer los archivos del frontend

### Logs

- **API**: Ver logs en la consola donde se ejecuta `main_api.py`
- **Nginx**: `/var/log/nginx/quinela_access.log` y `/var/log/nginx/quinela_error.log`
- **Frontend**: Abrir DevTools del navegador para ver errores JavaScript

## Docker

### Docker Compose (Recomendado)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

La configuración de compose incluye:

- **quinela-app**: Aplicación web principal
- **quinela-scraper**: Servicio automatizado de recolección de datos
- **nginx**: Proxy reverso para producción

### Build Manual de Docker

```bash
# Construir imagen
docker build -t quiniela-sarco .

# Ejecutar contenedor
docker run -p 5000:5000 -v $(pwd)/data:/app/data quiniela-sarco
```

## Configuración

### Variables de Entorno

| Variable                    | Predeterminado                        | Descripción                       |
| --------------------------- | ------------------------------------- | ---------------------------------- |
| `DATABASE_PATH`           | `data/quinela.db`                   | Ubicación de base de datos SQLite |
| `SCRAPING_URL`            | `https://www.jugandoonline.com.ar/` | Sitio web fuente                   |
| `SCRAPING_INTERVAL_HOURS` | `1`                                 | Frecuencia de scraping             |
| `FLASK_HOST`              | `0.0.0.0`                           | Host de Flask                      |
| `FLASK_PORT`              | `5000`                              | Puerto de Flask                    |
| `FLASK_DEBUG`             | `False`                             | Modo debug                         |
| `LOG_LEVEL`               | `INFO`                              | Nivel de logging                   |

### Estructura de Directorios

### Estructura de Archivos

```text
quinela-wp/
├── config.py              # Gestión de configuración
├── requirements.txt       # Dependencias de Python
├── docker-compose.yml     # Orquestación de Docker
├── Dockerfile            # Definición de contenedor
├── backend/              # Módulos principales del backend
│   ├── api.py           # Rutas de la API Flask
│   ├── database.py      # Operaciones SQLite
│   ├── analytics.py     # Análisis estadístico
│   └── scraper.py       # Recolección de datos
├── data/                # Base de datos SQLite (auto-creada)
├── logs/                # Logs de aplicación (auto-creados)
└── frontend/            # Assets estáticos (expansión futura)
```

### Análisis de Frecuencia Mensual

- Rastrea la frecuencia de números para el mes actual
- Calcula porcentajes de aparición
- Proporciona métricas estadísticas (media, mediana, máx, mín)

### Detección de Números Hot/Cold

- Identifica números en tendencia (hot)
- Encuentra números con bajo rendimiento (cold)
- Utiliza umbrales estadísticos basados en desviación estándar

### Reconocimiento de Patrones Semanales

- Analiza patrones por día de la semana
- Proporciona recomendaciones específicas por día
- Análisis de tendencias históricas

### Recomendaciones Inteligentes

- Combina múltiples métodos de análisis
- Puntuación de confianza para cada recomendación
- Incluye estrategias contrarias
- Razonamiento transparente para cada predicción

## Contribuir

1. Hacer fork del repositorio
2. Crear una rama de característica (`git checkout -b feature/caracteristica-increible`)
3. Hacer commit de tus cambios (`git commit -m 'Agregar característica increíble'`)
4. Push a la rama (`git push origin feature/caracteristica-increible`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Créditos

- **Creador Original**: [matiasdante](https://github.com/matiasdante)
- **Fuente de Datos**: [Jugando Online](https://www.jugandoonline.com.ar/)
- **Análisis Mejorado**: Análisis estadístico avanzado e interfaz web moderna

---

### Hecho con ❤️ para un mejor análisis de lotería
