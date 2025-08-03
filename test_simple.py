import requests

def test_simple_api():
    """Test de l'API simple"""
    print("🔄 Test de l'API simple...")
    
    # Test de l'endpoint racine
    try:
        response = requests.get("http://localhost:8001/", timeout=5)
        print(f"✅ Endpoint racine: {response.status_code}")
        print(f"📄 Message: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ API non accessible sur le port 8001")
        return
    
    # Test de l'endpoint generate
    test_data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@email.com",
        "poste_vise": "Développeur Python",
        "experience": "5 ans d'expérience en développement web"
    }
    
    print("\n🔄 Test de génération de lettre...")
    try:
        response = requests.post(
            "http://localhost:8001/generate",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération réussie!")
            print(f"📝 Lettre générée: {len(data.get('lettre', ''))} caractères")
            print("\n📄 Lettre complète:")
            print("=" * 50)
            print(data.get('lettre', ''))
            print("=" * 50)
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple_api() 