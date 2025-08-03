from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
import uvicorn
from transformers import pipeline
import torch
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

# Création de l'application FastAPI
app = FastAPI(
    title="API CV Generator",
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

# Variable globale pour le pipeline
text_generator = None

def initialize_model():
    """Initialise le modèle HuggingFace"""
    global text_generator
    try:
        print("🔄 Initialisation du modèle HuggingFace...")
        text_generator = pipeline(
            "text-generation",
            model="tiiuae/falcon-7b-instruct",
            torch_dtype=torch.bfloat16,
            device_map="auto",
            max_length=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        print("✅ Modèle initialisé avec succès!")
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du modèle: {e}")
        print("⚠️ Utilisation d'un modèle de fallback...")
        try:
            text_generator = pipeline(
                "text-generation",
                model="gpt2",
                max_length=200,
                do_sample=True,
                temperature=0.8
            )
            print("✅ Modèle de fallback initialisé!")
        except Exception as e2:
            print(f"❌ Erreur avec le modèle de fallback: {e2}")
            text_generator = None

def generate_letter(data: CVRequest) -> str:
    """
    Génère une lettre de motivation en utilisant le modèle HuggingFace
    """
    if text_generator is None:
        return "Erreur: Modèle non disponible. Veuillez réessayer plus tard."
    
    try:
        # Formation du prompt
        prompt = f"Génère une lettre de motivation pour un poste de {data.poste_vise}. Nom : {data.nom} {data.prenom}. Email : {data.email}. Expérience : {data.experience}"
        
        print(f"🔄 Génération de la lettre avec le prompt: {prompt[:100]}...")
        
        # Génération du texte
        result = text_generator(prompt, max_length=512, do_sample=True, temperature=0.7)
        
        # Extraction du texte généré
        generated_text = result[0]['generated_text']
        
        # Nettoyage du texte (suppression du prompt original)
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()
        
        print(f"✅ Lettre générée avec succès! Longueur: {len(generated_text)} caractères")
        return generated_text
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return f"Erreur lors de la génération de la lettre: {str(e)}"

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
    Affiche les informations dans la console et retourne le fichier PDF
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
        lettre = generate_letter(request)
        
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

@app.on_event("startup")
async def startup_event():
    """Événement de démarrage pour initialiser le modèle"""
    initialize_model()

if __name__ == "__main__":
    # Lancement du serveur avec uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
