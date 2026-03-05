
# Technologies to use

## python 3.12-slim
- uv to manage dependenies
- FastAPI
- uvicorn to run the server port 80
- Dependencias del proyecto (pyproject.toml)

## Makefile to manage tasks
- dev (uvicorn app.server:app --reload --host 0.0.0.0 --port 80)
- test (pytest)
- build (docker build -t novadynamics .)
- deploy (docker compose up --build -d)

## docker-compose
- dockerfile to build and run project
- docker-compose.yml to run the container
- .env.example to manage environment variables

## gitignore
- .env
- .venv
- __pycache__
- .pytest_cache
- .coverage
- htmlcov
- dist
- build
- .DS_Store
- .idea
- .vscode

# work flow

you create a endpoint "/" on server.py that return a json with the following structure:
```json
{
  "status": "ok"
}
```

Create other service on server.py and expose a GET endpoint  "/schema_guardian"  with the following workflow:


## 1. consume services 
- https://designsuccess-media.s3.us-west-1.amazonaws.com/employee_records-dummy.json
- response structure 
```json
{
  "collection": "employee_records",
  "fields": [
    {
      "field": "id",
      "type": "uuid",
      "meta": {
        "note": "Primary key for the record",
        "interface": "input"
      }
    },
    ...
```

## 2. Analysis
- It must scan the schema for fields that lack a "meta.description" or "meta.note."

## 3.  AI Action: 
For every field missing a description, it must use an LLM (mock the call if needed) to generate a helpful description based on the field name (e.g., field user_dob -> AI Description: "The user's date of birth used for age verification").
- use OpenRouter with any model free and expose api key "OPENROUTER_API_KEY" in .env.example


## 4. Reporting: 
- It should output a report in json format listing what changes it suggests.

json
```json

{
  "collection": "employee_records",
  "total_fields": 15,
  "fields_missing_metadata": 5,
  "report": "# Schema Guardian Report\n\n| Field | Suggested Description |\n|---|---|\n| user_dob | The user's date of birth... |"
}
```

## 5. publish
- Add a README.md file with the following information (short and concise):
-- project name
-- description
-- installation 
-- usage 
-- license ( CMS Expert (Directus) Technical Assessment for Recruiting by Jose Ricardo Soler Hernandez)
- Add push the code on "https://github.com/risolerh/novadynamics.git"