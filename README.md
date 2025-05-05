# ProyectoETS
Este es nuestro proyecto de ETS para 1ºDAW en IES Puerto de La Cruz 2025

1. Tecnologías recomendadas
Lenguaje: Python 3.11+


Scraping/API: requests, BeautifulSoup o alguna API de tienda (si existe)


Persistencia: SQLite o PostgreSQL con SQLAlchemy


Notificaciones Telegram: python-telegram-bot o telepot


Tareas periódicas: APScheduler o Celery (si necesitas concurrencia real)


API REST: FastAPI


Testing: pytest


Gestión de dependencias: Poetry


Contenedores: Docker


Documentación: Markdown + PlantUML o UMLet + Diagrama de despliegue (Docker + FastAPI + DB)


3. Funcionalidades mínimas
a. 
Seguimiento de productos
Guardar productos con talla específica


Comprobar el precio en intervalos definidos


Detectar cambios de precio


Guardar histórico (últimos 10 + estadísticas: min, max, avg)


b. 
Notificaciones
Conexión con bot de Telegram


Envío inmediato al usuario cuando hay cambio de precio


c. 
Persistencia
Base de datos para:


Productos


Historial de precios


Configuración de usuarios


d. 
Configuración por usuario
Qué productos seguir


Intervalo de comprobación (por producto o usuario)


e. 
API REST (opcional pero recomendada)
Endpoints para:


Añadir/quitar productos


Consultar histórico


Consultar configuración



4. Calidad y pruebas
Usa pytest + pytest-cov para asegurar cobertura >90%


Tests unitarios: lógica de comparación de precios, scrapers, etc.


Tests de integración: base de datos + notificaciones



5. Despliegue y contenedores
Dockerfile + docker-compose con FastAPI, DB y tareas programadas


.env para manejar los tokens de forma segura
