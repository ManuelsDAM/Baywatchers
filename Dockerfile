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

# Ejecutar baywatchers.py con poetry
CMD ["poetry", "run", "python", "baywatchers.py"]
