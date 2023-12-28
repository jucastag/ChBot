# Usa una imagen base de Python
FROM python:3.11-slim-buster

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos al contenedor
COPY . .

# Establece el comando predeterminado para ejecutar la aplicación
CMD [ "python", "chatPdfWeb.py" ]