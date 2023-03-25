import json
import logging
from typing import List, Dict, Any
import gc

from modules.classifier import ClassifierFactory
from modules.output_postprocessor.output_preproc import Prediction


class PredictionService:

    def __init__(self, model_name: str) -> None:
        self.classifier = ClassifierFactory.get(model_name)

    def get_predictions(self, request_body: List[Dict[str, Any]]) -> Dict[str, Any]:
        logging.info("Obtaining predictions...")
        pred_list = self.classifier.predict(request_body)
        logging.info("Done!")
        resp = self._ok_response(pred_list)
        logging.info(json.dumps(resp, indent=4))
        gc.collect()
        return resp

    def _ok_response(self, pred_list: List[Prediction]) -> Dict[str, Any]:
        return {
            "code": 200,
            "response": {
                "model_name": self.classifier.name,
                "model_version": self.classifier.version,
                "results": [res.to_json() for res in pred_list]
            }
        }
