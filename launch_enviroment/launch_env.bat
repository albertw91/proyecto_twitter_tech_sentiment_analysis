
@echo off

rem Ruta y archivo a evaluar
set "ruta=.\venv"
echo "Evaluando la existencia del env en la %ruta%"


rem Si la ruta y el archivo existen, no se hace nada
if exist "%ruta%" (
  echo "La ruta y el archivo '%ruta%' existen. Actualizando requirements.txt"
  call .\venv\Scripts\activate.bat  
  python -m pip install -r requirements.txt
  
  
) else (
  echo "La ruta y el archivo '%ruta%' no existen. Creando venv e instalando requirements.txt..."
  python -m venv .\venv --python="C:\python\python312\python.exe
  call .\venv\Scripts\activate.bat
  pip install -r requirements.txt
  echo "Proceso terminado. Se ha instalado requirements.txt"
  start .\venv\Scripts\activate.bat
)



echo "."


