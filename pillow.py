import requests

name = requests.get("https://www.google.com")

print(name.content)