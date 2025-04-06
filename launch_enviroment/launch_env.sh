#!/bin/bash

# Ruta a evaluar
ruta="./venv"

# Si la ruta existe, se activa el venv e instala requirements.txt
if [ -d "$ruta" ]; then
  echo "La ruta '$ruta' existe."
  echo "Activando el entorno virtual..."
   if ! source ./venv/Scripts/activate; then
    source ./venv/Scripts/activate
    echo "No se pudo inicializar el entorno"
    exit 1
    else
      source ./venv/Scripts/activate
  fi
  echo "Instalando dependencias..."
  pip install -r requirements.txt
else
  echo "La ruta '$ruta' no existe. Creando el entorno virtual..."
  C:/python/python3118/python.exe -m venv ./venv
  echo "Activando el entorno virtual..."
  if ! source ./venv/Scripts/activate; then
    source ./venv/Scripts/activate
    echo "No se pudo inicializar el entorno"
    exit 1
    else
      source ./venv/Scripts/activate
  fi
  echo "Instalando dependencias..."
  pip install -r requirements.txt
fi

echo "Proceso finalizado."