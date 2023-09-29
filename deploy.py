import os
import requests
import subprocess

# Récupération des informations d'authentification
username = os.environ['PYTHONANYWHERE_USERNAME']   
token = os.environ['PYTHONANYWHERE_API_KEY']
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

subprocess.run("source venv/bin/activate", shell=True)




def deploy():
  build()
  push_code()
  deploy_to_pythonanywhere()
  restart_app()

def build():
  subprocess.run("python manage.py collectstatic --noinput", shell=True)

def push_code():
  subprocess.run(f"git push https://{username}:{token}@github.com/DMTJosue/tricyclebooking.git", shell=True)

def deploy_to_pythonanywhere():
  subprocess.run(f"git push https://{username}:{token}@git.pythonanywhere.com/DMTJosue/tricyclebooking.git", shell=True)

def deploy_to_pythonanywhere():

  headers = {"Authorization": f"Token {token}"}

  # Récupérer la liste des apps
  response = requests.get(
    f"https://www.pythonanywhere.com/api/v0/user/{username}/apps/",
    headers=headers
  )

  # Récupérer l'ID de l'app
  apps = response.json()
  app_id = apps[0]['id']  

  # Déployer le code
  response = requests.post(
    f"https://www.pythonanywhere.com/api/v0/user/{username}/apps/{app_id}/deploy/",
    headers=headers
  )

  if response.status_code == 201:
    print("Déploiement réussi!")
  else:
    print("Erreur de déploiement")

def restart_app():
  headers = {"Authorization": f"Token {token}"}

  response = requests.post(
    f"https://www.pythonanywhere.com/api/v0/user/{username}/restart/",
    headers=headers
  )

  if response.status_code == 200:
    print("Application restarted!")
  else:
    print("Error restarting app")
    
if __name__ == '__main__':
  deploy()


