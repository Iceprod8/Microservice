# Utiliser une image Python de base
FROM python:3.9.20-alpine3.19

# Installer les dépendances
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

# Expose le port pour le Gateway
EXPOSE 80

# Commande pour lancer l'application
CMD ["python", "app.py"]
