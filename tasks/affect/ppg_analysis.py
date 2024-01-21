"""
Affect - Physical activity analysis
"""
import json
from typing import Any
from typing import List

import neurokit2 as nk
import pandas as pd

from tasks.affect.base import Affect


class PPGAnalysis(Affect):
    """
    **Description:**

        This tasks performs hrv analysis on the provided raw ppg affect data for specific patient.
    """

    name: str = "affect_ppg_analysis"
    chat_name: str = "AffectPPGAnalysis"
    description: str = (
        "When a request for analysis of ppg data is received, "
        "call this analysis tool. This tool is specifically designed to perform hrv analysis on ppg records, "
    )
    dependencies: List[str] = ["affect_ppg_get"]
    inputs: List[str] = [
        "You should provide the data source, which is in form of datapipe:datapipe_key "
        "the datapipe_key should be extracted from the result of previous actions.",
    ]
    outputs: List[str] = [
        "returns an array of json objects which contains the following keys:"
        "\n**HRV_MeanNN**: The mean of the RR intervals."
        "\n**HRV_SDNN**: The standard deviation of the RR intervals.",
        "\n**HRV_RMSSD**: The square root of the mean of the squared successive differences between adjacent RR intervals.",
        "\n**HRV_SDSD**: The standard deviation of the successive differences between RR intervals.",
        "\n**HRV_CVNN**: The standard deviation of the RR intervals (SDNN) divided by the mean of the RR intervals",
        "\n**HRV_CVSD**: The root mean square of successive differences (RMSSD) divided by the mean of the RR intervals",
        "\n**HRV_MedianNN**: The median of the RR intervals.",
        "\n**HRV_MadNN**: The median absolute deviation of the RR intervals.",
        "\n**HRV_MCVNN** The median absolute deviation of the RR intervals (MadNN) divided by the median of the RR intervals",
        "\n**HRV_IQRNN** The interquartile range (IQR) of the RR intervals.",
        "\n**HRV_Prc80NN**: The 80th percentile of the RR intervals.",
        "\n**HRV_pNN50**: The proportion of RR intervals greater than 50ms, out of the total number of RR intervals.",
        "\n**HRV_pNN20**: The proportion of RR intervals greater than 20ms, out of the total number of RR intervals.",
        "\n**HRV_MinNN**: The minimum of the RR intervals.",
        "\n**HRV_MaxNN**: The maximum of the RR intervals.",
        "\n**HRV_HTI**: The HRV triangular index, measuring the total number of RR intervals divided by the height of the RR intervals histogram.",
        "\n**HRV_LF**: The spectral power of low frequencies (by default, .04 to .15 Hz).",
        "\n**HRV_PSS**: Percentage of short segments.",
        "\n**HRV_HF**: The spectral power of high frequencies (by default, .15 to .4 Hz).",
        "\n**HRV_VHF**: The spectral power of very high frequencies (by default, .4 to .5 Hz).",
        "\n**HRV_LFHF**: The ratio obtained by dividing the low frequency power by the high frequency power.",
        "\n**HRV_LFn**: The normalized low frequency, obtained by dividing the low frequency power by the total power.",
        "\n**HRV_HFn**: The normalized high frequency, obtained by dividing the low frequency power by the total power.",
        "\n**HRV_LnHF**: The log transformed HF.",
        "\n**HRV_SD1**: Standard deviation perpendicular to the line of identity. It is an index of short-term RR interval fluctuations, i.e.,"
        "beat-to-beat variability. It is equivalent (although on another scale) to RMSSD, "
        "and therefore it is redundant to report correlation with both.",
        "\n**HRV_SD2** Standard deviation along the identity line. Index of long-term HRV changes.",
        "\n**HRV_SD1SD2**: The ratio of SD1 to SD2. Describes the ratio of short term to long term variations in HRV.",
        "\n**HRV_S**: Area of ellipse described by SD1 and SD2 (pi * SD1 * SD2). It is proportional to SD1SD2.",
        "\n**Heart_Rate** the mean heart rate after stimulus onset.",
    ]
    # False if the output should directly passed back to the planner.
    # True if it should be stored in datapipe
    output_type: bool = True

    def _execute(
        self,
        inputs: List[Any] = None,
    ) -> str:
        ppg = json.loads(inputs[0]["data"])
        df = None
        for i in range(0, len(ppg), 60 * 20):
            ppgs = [p["ppg"] for p in ppg[i : i + 60 * 20]]
            ppg_signals, info = nk.ppg_process(ppgs, sampling_rate=20)
            if df is None:
                df = nk.ppg_analyze(ppg_signals, sampling_rate=20)
            else:
                df = pd.concat(
                    [
                        df,
                        nk.ppg_analyze(ppg_signals, sampling_rate=20),
                    ],
                    axis=0,
                    ignore_index=True,
                )
        df.dropna(how="all", axis=1, inplace=True)
        df = df[
            [
                "HRV_MeanNN",
                "HRV_SDNN",
                "HRV_RMSSD",
                "HRV_SDSD",
                "HRV_CVNN",
                "HRV_CVSD",
                "HRV_MedianNN",
                "HRV_MadNN",
                "HRV_MCVNN",
                "HRV_IQRNN",
                "HRV_Prc80NN",
                "HRV_pNN50",
                "HRV_pNN20",
                "HRV_MinNN",
                "HRV_MaxNN",
                "HRV_TINN",
                "HRV_HTI",
                "HRV_LF",
                "HRV_PSS",
                "HRV_HF",
                "HRV_VHF",
                "HRV_LFHF",
                "HRV_LFn",
                "HRV_HFn",
                "HRV_LnHF",
                "HRV_SD1",
                "HRV_SD2",
                "HRV_SD1SD2",
                "HRV_S",
                "PPG_Rate_Mean",
            ]
        ]
        df["HRV_PSS"] = df["HRV_LF"]
        hr = df["PPG_Rate_Mean"].mean()
        df = (df - df.min()) / (df.max() - df.min())
        df = df.mean()
        df["Heart_Rate"] = hr
        df = df.round(2)
        json_out = df.to_json(orient="columns")
        return json_out
