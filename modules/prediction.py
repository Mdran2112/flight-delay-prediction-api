import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class Prediction:
    flight_id: int
    label_str: Optional[str] = None

    def __post_init__(self):
        ...

    def to_json(self) -> Dict[str, Any]:
        """return {
                    "observation_id": self.observation_id,
                    "label": self.label_str
                }"""

        return json.loads(json.dumps(asdict(self)))

