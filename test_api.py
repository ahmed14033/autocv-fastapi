import requests
import json

# URL de l'API
BASE_URL = "http://localhost:8000"

def test_api():
    """Test de l'API FastAPI"""
    
    # Test de l'endpoint racine
    print("=== Test de l'endpoint racine ===")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API. Assurez-vous que le serveur est démarré.")
        return
    
    print("\n=== Test de l'endpoint /generate ===")
    
    # Données de test
    test_data = {
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@email.com",
        "poste_vise": "Développeur Python",
        "experience": "5 ans d'expérience en développement web"
    }
    
    try:
        # Test de l'endpoint POST /generate
        response = requests.post(
            f"{BASE_URL}/generate",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        response_data = response.json()
        print(f"Status: {response_data.get('status')}")
        print(f"Lettre générée: {response_data.get('lettre', 'Non disponible')[:200]}...")
        
        if response.status_code == 200:
            print("✅ Test réussi !")
            if response_data.get('lettre'):
                print(f"📝 Longueur de la lettre: {len(response_data['lettre'])} caractères")
        else:
            print("❌ Test échoué !")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_api() 