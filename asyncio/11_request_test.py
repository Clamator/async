from getpass import getpass

import requests

with requests.Session() as session:
    auth_response = requests.get('https://rutracker.org/forum/index.php', auth=('gorindos', getpass()))
    auth_response.json()