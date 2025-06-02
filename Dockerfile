FROM python:3.13

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Crear y usar el directorio de trabajo
WORKDIR /app

# Copiar archivos necesarios para instalar dependencias
COPY pyproject.toml poetry.lock* /app/

# Copiar el resto del código fuente
COPY . .

# Configurar Poetry para no crear entornos virtuales dentro del contenedor
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Ejecutar la API con uvicorn
CMD ["poetry", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
