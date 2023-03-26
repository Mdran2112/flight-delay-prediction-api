from typing import List, Dict, Any

from modules.classifier import ClassifierFactory
from modules.prediction import Prediction


class PredictionService:
    """
    Executes prediction workflow and wraps the results in a json response.
    Args:
        model_name: Name of the prediction model.

    The model's folder has to be located in MODELS_BASEPATH, and has to be
    named as the model itself. Inside model's folder, two files must be founded: <model_name>.pkl and
    <model_name>_metadata.json
    The json metadata has information related with model, such as version, classes, output processing strategy, etc.
    """
    def __init__(self, model_name: str) -> None:
        self.classifier = ClassifierFactory.get(model_name)

    def get_predictions(self, request_body: List[Dict[str, Any]]) -> Dict[str, Any]:
        #logging.info("Obtaining predictions...")
        pred_list = self.classifier.predict(request_body)
        resp = self._ok_response(pred_list)
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
