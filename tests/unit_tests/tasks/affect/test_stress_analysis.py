import json

from tasks.affect import StressAnalysis


def test_ppg_analysis_execute():
    data = {
        "HRV_MeanNN": 0.33,
        "HRV_SDNN": 0.31,
        "HRV_RMSSD": 0.34,
        "HRV_SDSD": 0.34,
        "HRV_CVNN": 0.52,
        "HRV_CVSD": 0.48,
        "HRV_MedianNN": 0.43,
        "HRV_MadNN": 0.35,
        "HRV_MCVNN": 0.58,
        "HRV_IQRNN": 0.52,
        "HRV_Prc80NN": 0.38,
        "HRV_pNN50": 0.54,
        "HRV_pNN20": 0.67,
        "HRV_MinNN": 0.29,
        "HRV_MaxNN": 0.26,
        "HRV_TINN": 0.22,
        "HRV_HTI": 0.44,
        "HRV_LF": 0.54,
        "HRV_PSS": 0.54,
        "HRV_HF": 0.39,
        "HRV_VHF": 0.35,
        "HRV_LFHF": 0.12,
        "HRV_LFn": 0.47,
        "HRV_HFn": 0.53,
        "HRV_LnHF": 0.73,
        "HRV_SD1": 0.34,
        "HRV_SD2": 0.27,
        "HRV_SD1SD2": 0.49,
        "HRV_S": 0.24,
        "PPG_Rate_Mean": 0.49,
        "Heart_Rate": 33.74,
    }
    stress_analysis_task = StressAnalysis()

    result = stress_analysis_task._execute(
        [{"data": json.dumps(data)}]
    )
    print("result/////", result)
    assert isinstance(result, int)
