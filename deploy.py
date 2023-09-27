import os
import requests
import zipfile

# Récupération des informations d'authentification
username = os.environ['PYTHONANYWHERE_USERNAME']   
token = os.environ['PYTHONANYWHERE_API_KEY']

try:

  # Création du fichier zip
  zipf = zipfile.ZipFile('project.zip', 'w', zipfile.ZIP_DEFLATED)  
  zipf.write('deploy.py')     
  zipf.write('requirements.txt')
  zipf.close()

  if os.path.exists('project.zip'):

    # Récupération de l'ID de l'application
    response = requests.get(
      f"https://www.pythonanywhere.com/api/v0/user/{username}/apps/", 
      headers={'Authorization': f'Token {token}'}
    )

    app_id = response.json()[0]['id']

    # Préparation des données de déploiement
    files = {'directory': open('project.zip', 'rb')}

    # Requête de déploiement
    response = requests.post(
      f"https://www.pythonanywhere.com/api/v0/user/{username}/apps/{app_id}/deploy/",  
      headers={'Authorization': f'Token {token}'},
      files=files
    )

    if response.status_code == 201:
      print("Déploiement réussi!")
    elif response.status_code == 400:  
      print("Requête invalide")
    else:
      print(f"Erreur {response.status_code}: {response.text}")

  else:
    print("Erreur de création du zip")

except requests.RequestException as e:
  print("Erreur réseau: ", e)
