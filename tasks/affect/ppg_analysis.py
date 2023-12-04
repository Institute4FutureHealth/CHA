from typing import List, Any
import pandas as pd
import neurokit2 as nk
from e2epyppg.e2e_ppg_pipeline import e2e_hrv_extraction
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
                          'RMSSD stands for the root mean square of successive differences. It measures the time difference between each successive heartbeat. RMSSD is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'pNN50 is the number of times successive heartbeat intervals exceed 50ms. It shows how active your parasympathetic system is relative to the sympathetic nervous system. pNN50 is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'LF is the Low-Frequency power of the interbeat intervals signal: frequency activity between 0.04 and 0.15Hz. LF is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'HF is the High-Frequency power of the interbeat intervals signal: frequency activity between 0.15 and 0.40Hz. HF is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          'LFHF is the ratio of Low Frequency (LF) to High Frequency (HF). it can be an indicative of Sympathetic to Parasympathetic Autonomic Balance. LFHF is an HRV parameter that can be used for stress analysis and cardiovascular health assessment.',
                          ]
    #False if the output should directly passed back to the planner.
    #True if it should be stored in datapipe
    output_type: bool = True

    revised_voi_names: List[str] = ['Heart rate', 'RMSSD', 'pNN50',
                                    'LF', 'HF', 'LFHF']


    def _hr_hrv_extraction(
            self,
            df_ppg: pd.DataFrame,
            sampling_frequency: int,
            revised_voi_names: List[str],
            hrv_extraction_method: str = 'neurokit',
    ) -> pd.DataFrame:
        sig = df_ppg['ppg'].values.astype(int)
        if hrv_extraction_method == 'neurokit':
            voi = ['PPG_Rate_Mean', 'HRV_RMSSD', 'HRV_pNN50', 'HRV_LF', 'HRV_HF', 'HRV_LFHF']
            preprocessed_data, _ = nk.ppg_process(sig, sampling_rate=sampling_frequency)
            df_hrv = nk.ppg_analyze(
                preprocessed_data, sampling_rate=sampling_frequency)[voi]
            df_hrv = df_hrv[voi]
            df_hrv.columns = revised_voi_names
            return df_hrv
        elif hrv_extraction_method == 'e2epyppg':
            voi = ['HR', 'HRV_RMSSD', 'HRV_pNN50', 'HRV_LF', 'HRV_HF', 'HRV_LFHF']
            try:
                df_hrv = e2e_hrv_extraction(
                    input_sig=sig,
                    sampling_rate=sampling_frequency,
                    window_length_sec=60,
                    peak_detection_method='nk'
                )[voi]
                df_hrv = df_hrv[voi]
                df_hrv.columns = revised_voi_names
                df_hrv = df_hrv.mean().to_frame().T
            except Exception as e:
                print('No clean PPG segments was detected!')
                raise
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
                                           revised_voi_names=self.revised_voi_names)
            df_voi = pd.concat([df_voi, temp], ignore_index=True)
        df_out = df_voi.mean().to_frame().T
        df_out = df_out.round(2)
        json_out = df_out.to_json(orient='records')
        return json_out
