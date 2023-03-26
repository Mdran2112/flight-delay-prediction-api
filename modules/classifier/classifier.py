import logging
from typing import Dict, Any, List, Optional

import pandas as pd
from sklearn.pipeline import Pipeline

from modules.output_postprocessor.output_preproc import OutputPostprocessor
from modules.prediction import Prediction


class Classifier:
    """
    Classification workflow wrapper.
    Args:
        pipeline: Scikit-learn pipeline for classification.
        model_metadata: dict with information regarding the model.
        post_processor: Output model processor.
    """

    def __init__(self, pipeline: Pipeline,
                 model_metadata: Dict[str, Any],
                 post_processor: Optional[OutputPostprocessor]) -> None:
        self.pipeline = pipeline
        self.model_metadata = model_metadata
        self.post_processor = post_processor
        self.name = model_metadata["name"]
        self.version = model_metadata["version"]
        self.classes = self.model_metadata["classes"]
        logging.info(f"model name: {self.name}")
        logging.info(f"model version: {self.version}")

    def _parse_prediction(self, y_pred: List[int],
                          obs_id_list: List[int]) -> List[Prediction]:
        predictions = []

        for pred, id in zip(y_pred, obs_id_list):
            predictions.append(Prediction(flight_id=id, label_str=self.classes[pred]))

        return predictions

    def predict(self, data: List[Dict[str, Any]]) -> List[Prediction]:
        obs_id_list = list(map(lambda obj: obj.pop("flight_id"), data))
        y_pred = self.pipeline.predict_proba(pd.DataFrame(data))  # get the scores for both classes
        y_pred = self.post_processor.do(y_pred)  # process the output model and define the class for each observation

        predictions = self._parse_prediction(y_pred, obs_id_list)  # List of Prediction objects

        return predictions
