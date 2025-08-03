import subprocess
import time
import requests
import sys

def launch_api_with_ai():
    """Lance l'API avec IA et attend que le modèle se charge"""
    print("🚀 Lancement de l'API avec IA...")
    
    # Lancement de l'API en arrière-plan
    try:
        process = subprocess.Popen([sys.executable, "main.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        print("⏳ Attente du chargement du modèle...")
        
        # Attendre que l'API soit prête
        for i in range(60):  # Attendre jusqu'à 60 secondes
            try:
                response = requests.get("http://localhost:8000/", timeout=2)
                if response.status_code == 200:
                    print("✅ API accessible!")
                    break
            except:
                pass
            
            time.sleep(1)
            if i % 10 == 0:
                print(f"⏳ Attente... ({i}s)")
        
        # Test de l'endpoint generate
        print("🔄 Test de génération avec IA...")
        test_data = {
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@email.com",
            "poste_vise": "Développeur Python",
            "experience": "5 ans d'expérience en développement web"
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/generate",
                json=test_data,
                timeout=120  # Timeout long pour la génération IA
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Génération IA réussie!")
                print(f"📝 Lettre générée: {len(data.get('lettre', ''))} caractères")
                print(f"📄 Début de la lettre: {data.get('lettre', '')[:200]}...")
            else:
                print(f"❌ Erreur: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout - Le modèle prend du temps à générer")
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")
        
        # Arrêter le processus
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

if __name__ == "__main__":
    launch_api_with_ai() 