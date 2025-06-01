@echo off
setlocal enabledelayedexpansion

:: Ruta al archivo plantuml.jar
set PLANTUML_JAR=plantuml-1.2025.2.jar

:: Carpeta de salida para los diagramas
set OUTPUT_DIR=diagrams

:: Formato de imagen
set FORMAT=png

:: Crear carpeta de salida si no existe
if not exist %OUTPUT_DIR% (
    mkdir %OUTPUT_DIR%
)

echo 🔍 Buscando archivos .puml en el proyecto...

:: Recorre recursivamente todos los archivos .puml
for /r %%f in (*.puml) do (
    echo 🛠️ Generando imagen para %%~nxf...

    :: Generar imagen en la carpeta diagrams con el mismo nombre de archivo
    java -jar %PLANTUML_JAR% -t%FORMAT% -o "%OUTPUT_DIR%" "%%f"
)

echo ✅ Todos los diagramas se han generado en la carpeta %OUTPUT_DIR%
pause