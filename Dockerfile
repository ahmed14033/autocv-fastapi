# Utilise une image Python légère
FROM python:3.11-slim

# Crée un dossier pour l'app
WORKDIR /app

# Copie les fichiers nécessaires dans le conteneur
COPY . .

# Installe les dépendances
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expose le port de l'app FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]
