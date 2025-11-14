# Dockerfile pour le projet Valorisation de Brevet

#dockerfile
# Utiliser Python 3.12 slim
FROM python:3.12-slim

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installer dépendances système
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port FastAPI
EXPOSE 5500

# Commande pour lancer le serveur
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "5500", "--reload"]


