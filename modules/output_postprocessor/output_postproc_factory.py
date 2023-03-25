import logging
from typing import Optional

from modules.output_postprocessor.output_preproc import OutputPostprocessor, ThresholdPredictionPostprocessor, \
    DefaultPredictionPostprocessor


class OutputPostprocessorFactory:
    SELECTOR = {
        "threshold": ThresholdPredictionPostprocessor,
        "default": DefaultPredictionPostprocessor,
        None: DefaultPredictionPostprocessor
    }

    @classmethod
    def get(cls, postproc_type: Optional[str], **kwargs) -> Optional[OutputPostprocessor]:
        postprocessor = cls.SELECTOR[postproc_type](**kwargs)
        logging.info(f"Building postprocessor: {postprocessor}")
        return postprocessor

