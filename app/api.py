import logging
import sys

from dotenv import load_dotenv

load_dotenv()
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s;%(levelname)s;%(message)s")

import json
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from fastapi import Security

from schemas import ObservationsModelModelBody
from utils.decorators import authorize, handle_error, ServiceNotReadyException
from services.prediction_service import PredictionService
import gc

PREDICTION_SERVICE: Optional[PredictionService] = None

DOCS_URL = f"/docs"
REDOC_URL = f"/redoc"

app = FastAPI(
    title="Flight Delay Prediction Server",
    description="REST API for predicting flights delay.",
    version="v0",
    contact={
        "name": "Martín Dran",
        "email": "dran2112@gmail.com",
    },
    docs_url=DOCS_URL,
    redoc_url=REDOC_URL)

URL_PREFIX = "/prediction-server"
api_key_header = APIKeyHeader(name='X-API-Key', auto_error=True)


@app.post(f"{URL_PREFIX}/predictions")
@authorize
@handle_error
def predictions(request_body: ObservationsModelModelBody, header: str = Security(api_key_header)):
    global PREDICTION_SERVICE
    if PREDICTION_SERVICE:
        body = list(map(lambda x: json.loads(x.json()), request_body.flights))
        resp = PREDICTION_SERVICE.get_predictions(body)
        return resp

    raise ServiceNotReadyException()


@app.put(f"{URL_PREFIX}/model/{{model_name}}")
@authorize
@handle_error
def change(model_name: str, header: str = Security(api_key_header)):
    global PREDICTION_SERVICE
    logging.info("Building PredictionService...")
    PREDICTION_SERVICE = PredictionService(model_name)
    gc.collect()
    resp = {
        "code": 200,
        "response": f"Changed model to {model_name}"
    }

    return resp


@app.get(f"{URL_PREFIX}/model")
@authorize
@handle_error
def model(header: str = Security(api_key_header)):
    global PREDICTION_SERVICE
    if PREDICTION_SERVICE:
        logging.info("Requesting model metadata...")
        metadata = PREDICTION_SERVICE.classifier.model_metadata
        return {
            "code": 200,
            "response": metadata
        }
    raise ServiceNotReadyException()


def run_api():
    uvicorn.run(
        "api:app",
        port=5050,
        host="0.0.0.0",
        loop='asyncio',
        workers=1
    )


if __name__ == "__main__":
    run_api()
