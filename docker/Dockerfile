# Usamos Python slim
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiamos requerimientos y los instalamos
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código
COPY ../ /app

# Creamos la carpeta de datos con permisos correctos
RUN mkdir -p /app/data && chmod 777 /app/data

# Ejecutamos el bot
CMD ["python", "bot.py"]
