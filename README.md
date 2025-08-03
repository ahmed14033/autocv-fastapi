# API CV Generator

Une API FastAPI pour générer des CV et lettres de motivation avec IA et PDF.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python main.py
```

L'API sera accessible sur `http://localhost:8000`

## Fonctionnalités

- **Génération de lettres de motivation** avec IA (HuggingFace)
- **Génération de fichiers PDF** avec ReportLab
- **Validation des données** avec Pydantic
- **Modèle de fallback** en cas d'erreur avec le modèle principal
- **Documentation interactive** Swagger UI

## Endpoints

### GET /
Endpoint racine pour tester l'API.

**Réponse :**
```json
{
  "message": "API CV Generator - Utilisez POST /generate"
}
```

### POST /generate
Endpoint pour générer un CV, une lettre de motivation et un PDF.

**Paramètres (JSON) :**
- `nom` (str) : Nom de la personne
- `prenom` (str) : Prénom de la personne  
- `email` (str) : Adresse email
- `poste_vise` (str) : Poste visé
- `experience` (str) : Expérience professionnelle

**Exemple de requête :**
```json
{
  "nom": "Dupont",
  "prenom": "Jean",
  "email": "jean.dupont@email.com",
  "poste_vise": "Développeur Python",
  "experience": "5 ans d'expérience en développement web"
}
```

**Réponse :**
- **Succès** : Fichier PDF `lettre_motivation.pdf`
- **Fallback** : JSON avec le texte de la lettre

## Modèles IA

L'API utilise les modèles suivants dans l'ordre de priorité :

1. **tiiuae/falcon-7b-instruct** - Modèle principal
2. **gpt2** - Modèle de fallback
3. **Message d'erreur** - Si aucun modèle n'est disponible

## Génération PDF

La fonction `create_pdf(letter_text: str)` :
- Utilise ReportLab pour générer un PDF professionnel
- Enregistre le fichier sous `lettre_motivation.pdf`
- Retourne le chemin du fichier
- Inclut mise en forme, styles et signature

## Test

Pour tester l'API :

```bash
# Version simple avec PDF
python main_simple_pdf.py
python test_pdf.py

# Version complète avec IA
python main.py
python test_api.py
```

## Documentation interactive

Une fois l'API lancée, vous pouvez accéder à la documentation interactive Swagger UI sur :
- `http://localhost:8000/docs` (version IA)
- `http://localhost:8002/docs` (version simple avec PDF)

## Validation des données

L'API utilise Pydantic pour valider automatiquement les données entrantes. Si les données sont invalides, l'API retournera une erreur 422 avec les détails de validation.

## Notes techniques

- Le modèle HuggingFace est initialisé au démarrage de l'API
- La génération peut prendre quelques secondes selon la complexité du prompt
- Les erreurs de modèle sont gérées gracieusement avec des messages d'erreur explicites
- Les fichiers PDF sont générés avec ReportLab pour une compatibilité maximale
- L'endpoint retourne directement le fichier PDF avec `FileResponse` 