



## Local testing
```
export GITHUB_REPOSITORY=gologic-partner/go-webapp-sample
export GITHUB_REPOSITORY_OWNER=gologic-partner
export GITHUB_TOKEN=xxxx
# This token permissions requirements is to be defined

python3 getghdata.py test.json

export DEFECTDOJO_API_TOKEN=xxxx
export DEFECTDOJO_IMPORT_API_URL=https://XXXXX/api/v2/import-scan/

python3 upload.py test.json
```