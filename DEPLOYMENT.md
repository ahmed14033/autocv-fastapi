# Guide de Déploiement Azure App Service

## 📋 Configuration

### Fichiers de Configuration Créés

1. **`main_autocv-fastapi.yml`** - GitHub Actions workflow
2. **`web.config`** - Configuration IIS pour Azure
3. **`.deployment`** - Configuration de déploiement
4. **`startup.txt`** - Commande de démarrage

### Commande Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100
```

**Paramètres :**
- `main:app` - Point d'entrée (module:variable)
- `-w 4` - 4 workers
- `-k uvicorn.workers.UvicornWorker` - Worker Uvicorn pour FastAPI
- `--bind 0.0.0.0:8000` - Écoute sur le port 8000
- `--timeout 120` - Timeout de 120 secondes
- `--keep-alive 5` - Keep-alive de 5 secondes
- `--max-requests 1000` - Max 1000 requêtes par worker
- `--max-requests-jitter 100` - Jitter pour éviter les redémarrages simultanés

## 🚀 Déploiement

### Option 1: GitHub Actions (Recommandé)

1. **Configurer les secrets GitHub :**
   - `AZURE_WEBAPP_PUBLISH_PROFILE` - Profil de publication Azure

2. **Modifier le nom de l'app :**
   ```yaml
   env:
     AZURE_WEBAPP_NAME: votre-app-name
   ```

3. **Pousser sur main :**
   ```bash
   git add .
   git commit -m "Deploy to Azure"
   git push origin main
   ```

### Option 2: Déploiement Manuel

1. **Créer l'App Service sur Azure Portal**
2. **Configurer les variables d'environnement :**
   - `WEBSITES_PORT=8000`
   - `PYTHONPATH=/home/site/wwwroot`

3. **Déployer via Azure CLI :**
   ```bash
   az webapp deployment source config-zip --resource-group <rg> --name <app-name> --src <zip-file>
   ```

## ⚙️ Configuration Azure App Service

### Variables d'Environnement

```bash
WEBSITES_PORT=8000
PYTHONPATH=/home/site/wwwroot
SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

### Configuration de l'Application

- **Runtime Stack :** Python 3.11
- **Startup Command :** Voir `startup.txt`
- **Port :** 8000

## 🔧 Dépannage

### Logs
- **Application Logs :** `/home/LogFiles/Application/`
- **Stdout Logs :** `/home/LogFiles/stdout`

### Vérifications
1. **Point d'entrée correct :** `main:app` ✅
2. **Workers configurés :** 4 workers ✅
3. **Worker Uvicorn :** `uvicorn.workers.UvicornWorker` ✅
4. **Port d'écoute :** 8000 ✅

## 📊 Monitoring

- **Métriques :** CPU, Memory, Requests
- **Logs :** Application, Access, Error
- **Health Check :** `/` endpoint

## 🎯 Points d'Entrée

- **GET /** - Health check
- **POST /generate** - Génération de lettre + PDF
- **GET /docs** - Documentation Swagger UI 