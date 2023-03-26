from abc import abstractmethod
from dataclasses import dataclass
from typing import List
import numpy as np


###############################################################################

class OutputPostprocessor:
    """
    Base class of model output postprocessing.
    """
    def __init__(self, **kwargs):
        ...

    @abstractmethod
    def _map_pred(self, pred: np.ndarray) -> List[int]:
        raise NotImplementedError()

    def do(self, pred: np.ndarray) -> List[int]:
        pred = self._map_pred(pred)
        return pred


@dataclass
class ThresholdPredictionPostprocessor(OutputPostprocessor):
    th: float

    def _map_pred(self, pred: np.ndarray) -> List[int]:
        """
        If class prediction score is greater than threshold, we will say that the
        observation belongs to the '1' class, otherwise the observation will be assigned to '0' class.
        """
        class_1_scores = pred[:, 1]  # grab the scores for class '1' (delayed)
        y_predict_class = [1 if score > self.th else 0 for score in class_1_scores]
        return y_predict_class


@dataclass
class DefaultPredictionPostprocessor(OutputPostprocessor):

    def _map_pred(self, pred: np.ndarray) -> List[int]:
        """
        The predicted class will be based on the argmax criteria.
        """
        y_predict_class = list(map(lambda x: x.argmax(), pred))
        return y_predict_class
