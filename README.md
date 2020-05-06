# Salient Object Detection API
## Purpose
Provide a Python API to detour pictures

## Anaconda local environment support
Install Anaconda:

See https://www.anaconda.com/distribution/#download-section

Edit `environment.yml` file and specify needed libraries

Install Anaconda local environment as below:
```bash
./install-conda-environment.sh
```
Activate Anaconda local environment as below:
```bash
conda activate ${PWD}/.conda
```

## Parameters
- **Configuration files**: yaml files are provided
    - development.yml
    - production.yml

The configuration file that will be used is based on ENVIRONMENT variable:
- **ENVIRONMENT**: environment of run
    - development
    - staging
    - production
    - *Default*: development
    
## Download pretrained model
Download basnet.pth model here & put it in project root :
<https://drive.google.com/uc?id=1s52ek_4YTDRt_EOkx1FS53u-vJa0c4nu&export=download>

    
## Run code
Run:
```bash
./entrypoint.sh
```
## Access route
Upload your file using 

<http://127.0.0.1:8000/detour>

and wait for save box (~seconds depending on image size)

## Swagger
You can find the API Swagger on host:port/docs 

<http://127.0.0.1:8000/docs/>
