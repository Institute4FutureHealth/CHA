from typing import List, Any
import pandas as pd
import neurokit2 as nk
from tasks.affect.base import Affect


class PpgAnalysis(Affect):
    name: str = "affect_ppg_analysis"
    chat_name: str = "AffectPpgAnalysis"
    description: str = ("Extract heart rate (HR) and heart rate variability (HRV) from Photoplethysmogram (PPG) signals. "
                        "You MUST call this when the user asks for HRV or HR or objective stress. "
                        )
    dependencies: List[str] = ["affect_ppg_get"]
    inputs: List[str] = ["datapipe key to the PPG data"]
    outputs: List[str] = ['Heart rate (HR) is the number of times heart beats per minute.',
                          'SDNN is the standard deviation of the interbeat intervals measured in ms. SDNN is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'RMSSD stands for the root mean square of successive differences. It measures the time difference between each successive heartbeat. RMSSD is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'pNN50 is the number of times successive heartbeat intervals exceed 50ms. It shows how active your parasympathetic system is relative to the sympathetic nervous system. pNN50 is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'LF is the Low-Frequency power of the interbeat intervals signal: frequency activity between 0.04 and 0.15Hz. LF is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'HF is the High-Frequency power of the interbeat intervals signal: frequency activity between 0.15 and 0.40Hz. HF is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'LFHF is the ratio of Low Frequency (LF) to High Frequency (HF). it can be an indicative of Sympathetic to Parasympathetic Autonomic Balance. LFHF is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'SD1 and RMSSD are identical heart rate variability metrics. It measures the time difference between each successive heartbeat. SD1 is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'SD2 measures short- and long-term HRV in ms and correlates with LF power. SD2 is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'SD1SD2 is the ratio of SD1 and SD2. It measures the unpredictability of the interbeat intervals. It is used to measure autonomic balance when the monitoring period is sufficiently long and there is sympathetic activation. SD1SD2 is correlated with the LFHF. SD1SD2 is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.'
                          ]
    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = True

    variable_of_interest: List[str] = ['PPG_Rate_Mean', 'HRV_SDNN', 'HRV_RMSSD', 'HRV_pNN50',
                                       'HRV_LF', 'HRV_HF', 'HRV_LFHF', 'HRV_SD1', 'HRV_SD2', 'HRV_SD1SD2']
    revised_voi_names: List[str] = ['Heart rate', 'SDNN', 'RMSSD', 'pNN50',
                                    'LF', 'HF', 'LFHF', 'SD1', 'SD2', 'SD1SD2']


    def _hrv_extraction(
            self,
            df_ppg: pd.DataFrame,
            sampling_frequency: int,
            parameters_of_interest: List[str],
            hrv_extraction_method: str = 'neurokit',
    ) -> pd.DataFrame:
        sig = df_ppg['ppg'].values.astype(int)
        if hrv_extraction_method == 'neurokit':
            preprocessed_data, _ = nk.ppg_process(sig, sampling_rate=sampling_frequency)
            df_hrv = nk.ppg_analyze(
                preprocessed_data, sampling_rate=sampling_frequency)[parameters_of_interest]
            return df_hrv
        else:
            raise ValueError('The PPG analysis method has not been defined!')


    def _execute(
        self,
        inputs: List[Any],
    ) -> str:
        df_ppg_chunks, sampling_frequency = self._json_to_ppg_dataframes_and_fs(
            json_data=inputs[0]['data'].strip())
        df_voi = pd.DataFrame(columns=self.revised_voi_names)
        for df_ppg in df_ppg_chunks:
            temp = self._hr_hrv_extraction(df_ppg=df_ppg,
                                           sampling_frequency=sampling_frequency,
                                           parameters_of_interest=self.variable_of_interest)
            temp = temp[self.variable_of_interest]
            temp.columns = self.revised_voi_names
            df_voi = pd.concat([df_voi, temp], ignore_index=True)
        df_out = df_voi.mean().to_frame().T
        df_out = df_out.round(2)
        json_out = df_out.to_json(orient='records')
        return json_out
