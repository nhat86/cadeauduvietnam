# Étape 1 : image Python
FROM python:3.11-slim

# Étape 2 : créer un dossier de travail
WORKDIR /app

# Étape 3 : copier requirements
COPY requirements.txt .

# Étape 4 : installer dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : copier le code
COPY . .

# Étape 6 : exposer le port
EXPOSE 8000

# Étape 7 : démarrer FastAPI avec uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
