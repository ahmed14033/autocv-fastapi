from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Création de l'application FastAPI
app = FastAPI(
    title="API CV Generator (Version Simple)",
    description="API pour générer des CV et lettres de motivation",
    version="1.0.0"
)

# Modèle Pydantic pour valider les données
class CVRequest(BaseModel):
    nom: str
    prenom: str
    email: str
    poste_vise: str
    experience: str

# Modèle de réponse
class CVResponse(BaseModel):
    status: str
    lettre: str

def generate_letter_simple(data: CVRequest) -> str:
    """
    Génère une lettre de motivation simple (sans IA pour les tests)
    """
    prompt = f"Génère une lettre de motivation pour un poste de {data.poste_vise}. Nom : {data.nom} {data.prenom}. Email : {data.email}. Expérience : {data.experience}"
    
    # Lettre de motivation générique basée sur les données
    lettre = f"""
Madame, Monsieur,

Je me permets de vous présenter ma candidature pour le poste de {data.poste_vise} au sein de votre entreprise.

Mon nom est {data.nom} {data.prenom} et je dispose de {data.experience}. Cette expérience m'a permis de développer des compétences solides dans mon domaine d'expertise.

Je suis particulièrement intéressé(e) par cette opportunité car elle correspond parfaitement à mes aspirations professionnelles et à mes compétences.

Vous pouvez me contacter à l'adresse suivante : {data.email}

Je reste à votre disposition pour un entretien et vous remercie de l'attention que vous porterez à ma candidature.

Cordialement,
{data.nom} {data.prenom}
"""
    
    return lettre.strip()

@app.get("/")
async def root():
    """Endpoint racine pour tester l'API"""
    return {"message": "API CV Generator - Utilisez POST /generate"}

@app.post("/generate", response_model=CVResponse)
async def generate_cv(request: CVRequest):
    """
    Endpoint pour générer un CV et une lettre de motivation
    """
    try:
        # Affichage des informations dans la console
        print("=== INFORMATIONS CV RECUES ===")
        print(f"Nom: {request.nom}")
        print(f"Prénom: {request.prenom}")
        print(f"Email: {request.email}")
        print(f"Poste visé: {request.poste_vise}")
        print(f"Expérience: {request.experience}")
        print("==============================")
        
        # Génération de la lettre
        lettre = generate_letter_simple(request)
        
        # Retourner le statut OK et la lettre
        return CVResponse(status="OK", lettre=lettre)
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

if __name__ == "__main__":
    # Lancement du serveur avec uvicorn
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8001,  # Port différent pour éviter les conflits
        reload=True,
        log_level="info"
    ) 