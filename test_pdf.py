import requests
import os

def test_pdf_api():
    """Test de l'API avec génération PDF"""
    print("🔄 Test de l'API avec PDF...")
    
    # Test de l'endpoint racine
    try:
        response = requests.get("http://localhost:8002/", timeout=5)
        print(f"✅ Endpoint racine: {response.status_code}")
        print(f"📄 Message: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ API non accessible sur le port 8002")
        return
    
    # Test de l'endpoint generate avec PDF
    test_data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@email.com",
        "poste_vise": "Développeur Python",
        "experience": "5 ans d'expérience en développement web"
    }
    
    print("\n🔄 Test de génération de lettre avec PDF...")
    try:
        response = requests.post(
            "http://localhost:8002/generate",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            # Vérifier le type de contenu
            content_type = response.headers.get('content-type', '')
            
            if 'application/pdf' in content_type:
                print("✅ PDF généré avec succès!")
                print(f"📄 Taille du PDF: {len(response.content)} bytes")
                
                # Sauvegarder le PDF pour vérification
                with open("test_lettre_motivation.pdf", "wb") as f:
                    f.write(response.content)
                print("💾 PDF sauvegardé sous 'test_lettre_motivation.pdf'")
                
                # Vérifier que le fichier existe
                if os.path.exists("test_lettre_motivation.pdf"):
                    file_size = os.path.getsize("test_lettre_motivation.pdf")
                    print(f"📊 Taille du fichier: {file_size} bytes")
                else:
                    print("❌ Fichier PDF non trouvé")
                    
            else:
                print("⚠️ Réponse JSON reçue (fallback)")
                data = response.json()
                print(f"📝 Lettre: {data.get('lettre', '')[:100]}...")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_pdf_api() 