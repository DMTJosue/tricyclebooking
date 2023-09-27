# Import des bibliothèques nécessaires
import os
import requests
import zipfile

# Récupération des informations d'authentification
username = os.environ['PYTHONANYWHERE_USERNAME']  
token = os.environ['PYTHONANYWHERE_API_KEY']

# Création du fichier zip contenant les fichiers à déployer
zipf = zipfile.ZipFile('project.zip', 'w', zipfile.ZIP_DEFLATED) 
# Ajout des fichiers deploy.py et requirements.txt
zipf.write('deploy.py')   
zipf.write('requirements.txt')
# Fermeture du fichier zip
zipf.close()

# Récupération de l'ID de l'application
response = requests.get(
  f"https://www.pythonanywhere.com/api/v0/user/{username}/apps/",
  headers={'Authorization': f'Token {token}'}
)
# Extraction de l'ID du premier élément de la réponse (liste d'apps)  
app_id = response.json()[0]['id']

# Préparation des données pour le déploiement  
files = {'directory': open('project.zip', 'rb')}

# Requête POST de déploiement
response = requests.post(
  f"https://www.pythonanywhere.com/api/v0/user/{username}/apps/{app_id}/deploy/",
  headers={'Authorization': f'Token {token}'},
  files=files
)

# Vérification du statut de la réponse
if response.status_code == 201:
  print("Déploiement réussi!")
else:
  print(f"Erreur de déploiement: {response.status_code}")
