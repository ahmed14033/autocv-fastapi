from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

# Création de l'application FastAPI
app = FastAPI(
    title="API CV Generator (Version Simple avec PDF)",
    description="API pour générer des CV et lettres de motivation avec PDF",
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

def create_pdf(letter_text: str) -> str:
    """
    Crée un fichier PDF à partir du texte de la lettre avec ReportLab
    """
    try:
        print("🔄 Création du fichier PDF...")
        
        # Création du fichier PDF
        pdf_path = "lettre_motivation.pdf"
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Styles personnalisés
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centré
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            leading=16
        )
        
        # Contenu du PDF
        story = []
        
        # Titre
        story.append(Paragraph("Lettre de Motivation", title_style))
        story.append(Spacer(1, 20))
        
        # Contenu de la lettre
        paragraphs = letter_text.strip().split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                story.append(Paragraph(paragraph.strip(), normal_style))
                story.append(Spacer(1, 12))
        
        # Signature
        story.append(Spacer(1, 30))
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=12,
            alignment=2  # Aligné à droite
        )
        story.append(Paragraph("Signature", signature_style))
        
        # Génération du PDF
        doc.build(story)
        
        print(f"✅ PDF créé avec succès: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du PDF: {e}")
        return None

@app.get("/")
async def root():
    """Endpoint racine pour tester l'API"""
    return {"message": "API CV Generator - Utilisez POST /generate"}

@app.post("/generate")
async def generate_cv(request: CVRequest):
    """
    Endpoint pour générer un CV, une lettre de motivation et un PDF
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
        
        # Création du PDF
        pdf_path = create_pdf(lettre)
        
        if pdf_path and os.path.exists(pdf_path):
            # Retourner le fichier PDF
            return FileResponse(
                path=pdf_path,
                filename="lettre_motivation.pdf",
                media_type="application/pdf"
            )
        else:
            # Fallback: retourner la réponse JSON si le PDF n'a pas pu être créé
            return CVResponse(status="OK", lettre=lettre)
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

if __name__ == "__main__":
    # Lancement du serveur avec uvicorn
    uvicorn.run(
        "main_simple_pdf:app",
        host="0.0.0.0",
        port=8002,  # Port différent pour éviter les conflits
        reload=True,
        log_level="info"
    ) 