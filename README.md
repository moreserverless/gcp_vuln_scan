# gcp_vuln_scan
Scans Docker images in a GCP project's artifact registry

## GCP API Services
Enable the following API services:

artifactregistry.googleapis.com    
cloudbuild.googleapis.com    
run.googleapis.com    
logging.googleapis.com   

### Using `gcloud`
```bash
gcloud services enable artifactregistry.googleapis.com \
      cloudbuild.googleapis.com \
      run.googleapis.com \
      logging.googleapis.com
```

## Run locally

1. Create a virtual env
    - `python3 -m venv venv`
2. Start virtual env
    - `. venv/bin/activate`
3. Install packages
    - `pip install -r requirements.txt`
  
## Deploy via `gcloud`
```bash
gcloud run deploy FUNCTION \
       --source . \
       --function FUNCTION_ENTRYPOINT \
       --base-image BASE_IMAGE \
       --region REGION
```

## Grafeas Documentation
[Python Client for Grafeas](https://googleapis.dev/python/grafeas/latest/)