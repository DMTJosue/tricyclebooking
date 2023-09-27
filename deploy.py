import os 
import requests

username = os.environ['PYTHONANYWHERE_USERNAME']
token = os.environ['PYTHONANYWHERE_API_KEY']

response = requests.get(
  f"https://www.pythonanywhere.com/api/v0/user/{username}/cpu/",
  headers={'Authorization': f'Token {token}'}
)

if response.status_code == 200:
  print('CPU quota info:')
  print(response.content)
else:
  print(f'Got unexpected status code {response.status_code}')
