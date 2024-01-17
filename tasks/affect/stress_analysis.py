"""
Affect - Physical activity analysis
"""
import json
from typing import Any
from typing import List

import torch

from tasks.affect.AE import AE
from tasks.affect.base import Affect
from tasks.affect.Predictor import Predictor


class StressAnalysis(Affect):
    """
    **Description:**

        This tasks performs hrv analysis on the provided raw ppg affect data for specific patient.
    """

    name: str = "affect_stress_analysis"
    chat_name: str = "AffectStressAnalysis"
    description: str = (
        "When a request for analysis of hrv data is received to estimate the stress level, "
        "call this analysis tool. This tool is specifically designed to perform stress analysis on hrv records, "
    )
    dependencies: List[str] = ["affect_ppg_analysis"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
    ]
    outputs: List[str] = [
        "returns the stress level out of 4. 0 is very low and 4 is very high. convert the number into proper interpretation."
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        hrv = json.loads(inputs[0]["data"])
        del hrv["Heart_Rate"]
        hrv = list(hrv.values())
        mAE = AE()
        mAE.load_state_dict(torch.load("models/AE_1.dict"))
        mAE.eval()

        mPredictor = Predictor()
        mPredictor.load_state_dict(
            torch.load("models/Predict_1.dict")
        )
        mPredictor.eval()

        encoded = mAE.encode(torch.FloatTensor(hrv))
        prediction = mPredictor(encoded)
        stress = torch.argmax(prediction, dim=0)
        return int(stress.detach())
