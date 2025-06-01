# Instalación y ejecución

## Requisitos
- Python 3.13
- Docker (opcional pero recomendado)
- Git

## Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/baywatchers.git
cd baywatchers

  ## Con Docker

docker build -t baywatchers .
docker run -p 8000:8000 baywatchers

##Manual, sin docker

pip install poetry
poetry install
python app/api/main.py

# Detener la app

docker ps          # El ID puede ser distinto en otro sistema
docker stop <11899767c769c99d66fb4cb6f2bd99c714c47025507f4ddd23570678d067bbd3>
```
:tm: :shipit: :recycle: :goberserk: