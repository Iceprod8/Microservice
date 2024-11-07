
# Utiliser une image officielle Python comme base
FROM python:3.9.20-alpine3.19

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

# Exposer le port 5000 pour Flask
EXPOSE 5000

# Commande pour démarrer l'application Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
