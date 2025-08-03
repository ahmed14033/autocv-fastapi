import requests
import time

def simple_test():
    """Test simple de l'API"""
    print("🔄 Test de l'API...")
    
    # Test de l'endpoint racine
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Endpoint racine: {response.status_code}")
    except:
        print("❌ API non accessible")
        return
    
    # Test de l'endpoint generate
    test_data = {
        "nom": "Test",
        "prenom": "User",
        "email": "test@test.com",
        "poste_vise": "Développeur",
        "experience": "2 ans"
    }
    
    print("🔄 Test de génération de lettre...")
    try:
        response = requests.post(
            "http://localhost:8000/generate",
            json=test_data,
            timeout=60  # Timeout plus long pour la génération
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Génération réussie!")
            print(f"📝 Lettre générée: {len(data.get('lettre', ''))} caractères")
            print(f"📄 Début de la lettre: {data.get('lettre', '')[:100]}...")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - Le modèle prend du temps à charger")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    simple_test() 