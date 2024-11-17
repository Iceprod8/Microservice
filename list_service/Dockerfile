# Utiliser une image officielle Python basée sur Debian
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Définir les variables d'environnement pour Flask
ENV FLASK_APP=app
ENV FLASK_ENV=development

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Ajouter le script wait-for-it.sh
RUN apt-get update && apt-get install -y curl && \
    curl -o /wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /wait-for-it.sh

# Exposer le port 5000 pour Flask
EXPOSE 5000

# Commande pour démarrer l'application Flask avec une attente pour PostgreSQL
CMD ["/wait-for-it.sh", "postgres:5432", "--", "flask", "run", "--host=0.0.0.0", "--port=5000"]
