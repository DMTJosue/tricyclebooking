import os
import requests
import subprocess

# Récupération des informations d'authentification
username = os.environ['PYTHONANYWHERE_USERNAME']   
token = os.environ['PYTHONANYWHERE_API_KEY']
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

def deploy():
  build()
  push_code()
  deploy_to_pythonanywhere()
  restart_app()

def build():
  subprocess.run("python manage.py collectstatic --noinput", shell=True)

def push_code():
  subprocess.run(f"git push https://{username}:{token}@github.com/user/repo.git", shell=True)

def deploy_to_pythonanywhere():
  subprocess.run(f"git push https://{username}:{token}@git.pythonanywhere.com/user/repo.git", shell=True)

def restart_app():
  requests.post(f"https://www.{username}.pythonanywhere.com/api/v0/user/{username}/restart/", headers={"Authorization": f"Token {token}"})

if __name__ == '__main__':
  deploy()
