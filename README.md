<h1 align="center">
  <br>
  <a href="https://github.com/matiasdante"><img src="https://www.loteria.gba.gov.ar/images/logos/01_LogoQuinielaMultiple.png" alt="DevOps Projects" width="200"></a>
  <br>
  Quiniela Analytics
  <br>
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

![Quiniela Analytics Dashboard](https://github.com/user-attachments/assets/dd7b6c36-b842-40e5-b5fa-67b85c673253)

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

## Instalación

### Requisitos Previos
- Python 3.11 o superior
- Git

### Inicio Rápido

1. **Clonar el repositorio**:
```bash
git clone https://github.com/matiasdante/quinela-wp.git
cd quinela-wp
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar entorno** (opcional):
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

## API

### Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Dashboard principal |
| `/api/current` | GET | Resultados actuales de lotería |
| `/api/scrape` | POST | Activador de scraping manual |
| `/api/analytics/monthly` | GET | Análisis de frecuencia mensual |
| `/api/analytics/hot-cold` | GET | Números hot y cold |
| `/api/analytics/weekly-patterns` | GET | Análisis de patrones semanales |
| `/api/recommendations` | GET | Recomendaciones inteligentes de números |
| `/api/patterns` | GET | Patrones detectados y alertas |
| `/api/historical` | GET | Resultados históricos |
| `/api/stats` | GET | Estadísticas de base de datos |
| `/api/provinces` | GET | Provincias disponibles |

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
      "min_frequency": 1
    }
  }
}
```

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
docker build -t quinela-analytics .

# Ejecutar contenedor
docker run -p 5000:5000 -v $(pwd)/data:/app/data quinela-analytics
```

## Configuración

### Variables de Entorno

| Variable | Predeterminado | Descripción |
|----------|----------------|-------------|
| `DATABASE_PATH` | `data/quinela.db` | Ubicación de base de datos SQLite |
| `SCRAPING_URL` | `https://www.jugandoonline.com.ar/` | Sitio web fuente |
| `SCRAPING_INTERVAL_HOURS` | `1` | Frecuencia de scraping |
| `FLASK_HOST` | `0.0.0.0` | Host de Flask |
| `FLASK_PORT` | `5000` | Puerto de Flask |
| `FLASK_DEBUG` | `False` | Modo debug |
| `LOG_LEVEL` | `INFO` | Nivel de logging |

### Estructura de Directorios
```
quinela-wp/
├── main.py                 # Punto de entrada principal de la aplicación
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

## Características de Análisis

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

<p align="center">
  <strong>Hecho con ❤️ para un mejor análisis de lotería</strong>
</p>
