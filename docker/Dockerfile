FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=America/Montevideo

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# crear carpeta para BD
RUN mkdir -p /app/data && chown -R nobody:nogroup /app/data

USER nobody
CMD ["python", "bot.py"]
