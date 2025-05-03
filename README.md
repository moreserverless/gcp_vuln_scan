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

## Sample return value

```txt
{'PROJECT_ID': {'IMAGE_NAME': {'med': [{'affected_package': 'org.apache.tomcat.embed:tomcat-embed-core',
     'affected_version': '10.1.40',
     'fixed_package': 'org.apache.tomcat.embed:tomcat-embed-core',
     'fixed_version': '11.0.0',
     'cve_description': 'CVE-2024-52317',
     'package_type': 'MAVEN'}],
   'high': [{'affected_package': 'sqlite',
     'affected_version': '3.48.0-r0',
     'fixed_package': 'sqlite',
     'fixed_version': '3.48.0-r1',
     'cve_description': 'CVE-2025-29087',
     'package_type': 'OS'},
    {'affected_package': 'binutils',
     'affected_version': '2.43.1-r1',
     'fixed_package': 'binutils',
     'fixed_version': '2.43.1-r2',
     'cve_description': 'CVE-2025-0840',
     'package_type': 'OS'}],
   'critical': []}}}
```