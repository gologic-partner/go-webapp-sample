# DefectDojo pipeline

# Github token permissions
I was only able to make it work with a Classic token with:
- repo.public_repo
- repo.security_events

## Local testing
```
export GITHUB_REPOSITORY=gologic-partner/go-webapp-sample
export GITHUB_REPOSITORY_OWNER=gologic-partner
export GITHUB_TOKEN=xxxx

python3 getghdata.py test.json

export DEFECTDOJO_API_TOKEN=xxxx
export DEFECTDOJO_IMPORT_API_URL=https://XXXXX/api/v2/import-scan/

python3 upload.py test.json
```