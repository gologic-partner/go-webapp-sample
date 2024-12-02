#Inspired from: https://dev.to/sirlawdin/automate-uploading-security-scan-results-to-defectdojo-7e4

import requests
import sys
import os

file_name = sys.argv[1]
# scan_type = 'github'

if file_name.endswith('.json'):
    scan_type = 'Github Vulnerability Scan'
elif file_name.endswith('.sarif'):
    scan_type = 'SARIF'
# elif file_name == 'semgrep.json':
#     scan_type = 'Semgrep JSON Report'

apitoken = os.environ.get('DEFECTDOJO_API_TOKEN')
headers = {
    'Authorization': 'Token ' + apitoken
}

url = os.environ.get('DEFECTDOJO_IMPORT_API_URL')
data = {
    'active': True,
    'verified': True,
    'scan_type': scan_type,
    'minimum_severity': 'Low',
    'engagement': 1
}

files = {
    'file': open(file_name, 'rb')
}

response = requests.post(url, headers=headers, data=data, files=files)

if response.status_code == 201:
    print('Scan results imported successfully')
else:
    print(f'Failed to import scan results: {response.content}')
