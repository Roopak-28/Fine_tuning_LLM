import requests
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Dict, Any
from pydantic import BaseModel
import traceback

class PipelineConfig(BaseModel):
    pipeline_name: str = "piercing_jun23a"
    pipeline_description: str = "ML pipeline for piercing"
    pipeline_json: Dict[str, Any] = {}

def get_access_token():
    url = "https://ig.aidtaas.com/mobius-iam-service/v1.0/login"

    payload = json.dumps({
      "userName": "aidtaas@gaiansolutions.com",
      "password": "Gaian@123",
      "productId": "c2255be4-ddf6-449e-a1e0-b4f7f9a2b636",
      "requestType": "TENANT"
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    try:
        result = response.json()
    except Exception:
        raise Exception(f"Failed to parse access token response: {response.text}")
    if "accessToken" not in result:
        raise Exception(f"Failed to get access token: {result}")
    return result['accessToken']

def create_pipeline(config):
    url = "https://ig.aidtaas.com/bob-service-test/v1.0/pipeline"

    payload = json.dumps({
      "name": config["pipeline_name"],
      "description": config['pipeline_description'],
      "jsonInput": [
        config['pipeline_json']
      ],
      "pipelineType": "ML"
    })
    headers = {
      'accept': 'application/json',
      'Authorization': f"Bearer {config['access_token']}",
      'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    print("Pipeline creation raw response:", response.text)
    try:
        result = response.json()
    except Exception:
        raise Exception(f"Failed to parse pipeline creation response as JSON: {response.text}")

    if 'pipelineId' not in result:
        raise Exception(f"Pipeline creation failed, response: {result}")

    return result['pipelineId']

def trigger_pipeline(config):
    url = f"https://ig.aidtaas.com/bob-service-test/v1.0/pipeline/trigger/ml?pipelineId={config['pipeline_id']}"

    payload = json.dumps({
        "pipelineType": "ML",
        "containerResources": {},
        "experimentId": config['experiment_id'],
        "enableCaching": True,
        "parameters": {},
        "version": 1
    })
    headers = {
        'accept': 'application/json',
        'Authorization': f"Bearer {config['access_token']}",
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=payload)
    print("Trigger pipeline raw response:", response.text)
    try:
        result = response.json()
    except Exception:
        raise Exception(f"Failed to parse trigger pipeline response as JSON: {response.text}")

    if 'runId' not in result:
        raise Exception(f"Pipeline trigger failed, response: {result}")

    return result['runId']

app = FastAPI()

# Global exception handler: shows Python errors in browser for easy debugging
@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    return PlainTextResponse(str(traceback.format_exc()), status_code=500)

@app.post("/run-pipeline")
def run_pipeline(config: PipelineConfig):
    try:
        config = config.dict()
        config['experiment_id'] = "37e5cbe2-9fd7-4bc1-ad49-86d8a4a2c2e3"
        config['access_token'] = get_access_token()
        pipeline_id = create_pipeline(config)
        config["pipeline_id"] = pipeline_id
        run_id = trigger_pipeline(config)
        result = {
            "pipeline_id": pipeline_id,
            "run_id": run_id
        }
        return result
    except Exception as e:
        # Also print the traceback in the logs
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run_pipeline:app", host="0.0.0.0", port=8000, reload=True)
