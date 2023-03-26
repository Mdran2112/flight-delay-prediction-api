import json
import logging
from os.path import join

import joblib

from utils.globals import MODELS_BASEPATH
from modules.classifier.classifier import Classifier
from modules.output_postprocessor import OutputPostprocessorFactory
from services.utils import check_if_file_existis


class ClassifierFactory:

    @classmethod
    def get(cls, model_name: str) -> Classifier:
        model_path = join(MODELS_BASEPATH, model_name, model_name + ".pkl")
        metadata_path = model_path.replace(".pkl", "_metadata.json")
        check_if_file_existis(model_path)
        check_if_file_existis(metadata_path)

        logging.info(f"loading pipeline model from {model_path}")

        pipe = joblib.load(model_path)

        logging.info(f"loading pipeline model metadata from {metadata_path}")

        with open(metadata_path, 'r') as jfile:
            metadata = json.load(jfile)

        postproc_type = metadata["post_proc"].get("type", None)
        postproc_params = metadata["post_proc"].get("params", {})

        postprocessor = OutputPostprocessorFactory.get(postproc_type, **postproc_params)

        logging.info("Creating Classifier...")
        classifier = Classifier(pipeline=pipe, model_metadata=metadata, post_processor=postprocessor)
        return classifier
