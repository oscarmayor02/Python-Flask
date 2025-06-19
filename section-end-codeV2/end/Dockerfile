FROM python:3.10  
# Usa la imagen oficial de Python 3.10 como base

EXPOSE 5000
# Expone el puerto 5000 para que la aplicación Flask sea accesible desde fuera del contenedor

WORKDIR /app  
# Establece el directorio de trabajo dentro del contenedor en /app

COPY ./requirements.txt requirements.txt  
# Copia el archivo de dependencias al contenedor

RUN pip install --no-cache-dir --upgrade -r requirements.txt  
# Instala las dependencias listadas en requirements.txt

COPY . . 
 # Copia todo el contenido del directorio actual al directorio de trabajo del contenedor

CMD ["flask", "run", "--host", "0.0.0.0"]  
# Comando por defecto para iniciar la aplicación Flask y hacerla accesible desde cualquier IP