# Notes

## Tools

- https://jsontopydantic.com/

## Initialising application:

```bash
 sam init --name insight-portfolio \ 
          --runtime python3.9 \
          --app-template hello-world \  --dependency-manager pip \  
          --tracing   
```

## Create and activate virtual environment

   ```bash
      virtualenv -p python3.9 env 
      .\env\Scripts\activate
   ```

## Install dependencies

```bash
  pip install fastapi[all] uvicorn mangum pandas yfinance
```

## Basic local test with uvicorn

```bash
  cd portfolios
  uvicorn main:api --reload
```

## Deploying application

```bash
 sam deploy -g --region eu-west-2  --stack-name investing-app
```
