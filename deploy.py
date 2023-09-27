import os
import requests
username = os.environ['PYTHONANYWHERE_USERNAME']
token = os.environ['PYTHONANYWHERE_API_KEY']
response = requests.get(
    'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
        username=username
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)
if response.status_code == 200:
    print('CPU quota info:')
    print(response.content)
elif response.status_code == 201:
  print("Déploiement réussi!")
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))