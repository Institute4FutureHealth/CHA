# import pytest
# from tasks.affect.sleep_analysis import SleepAnalysis
# import pandas as pd
# @pytest.fixture
# def sleep_analysis_instance():
#     return SleepAnalysis()
# def test_execute_average_analysis(sleep_analysis_instance):
#     # Test case for average analysis
#     input_data = {'data': '{"date": ["2023-01-01", "2023-01-02"], "total_sleep_time": [480, 500], '
#                           '"awake_duration": [20, 15]}'}
#     analysis_type = 'average'
#     result_json = sleep_analysis_instance._execute([input_data, analysis_type])
#     result_df = pd.read_json(result_json, orient='records')
#     # Define the expected DataFrame for average analysis
#     expected_df = pd.DataFrame({'total_sleep_time': [490.0], 'awake_duration': [17.5]})
#     result_df['total_sleep_time'] = result_df['total_sleep_time'].astype('float64')
#     # Check if the result DataFrame is equal to the expected DataFrame
#     pd.testing.assert_frame_equal(result_df, expected_df)
# def test_execute_invalid_analysis_type(sleep_analysis_instance):
#     # Test case for invalid analysis type
#     input_data = {'data': '{"date": ["2023-01-01", "2023-01-02"], "total_sleep_time": [480, 500], '
#                           '"awake_duration": [20, 15]}'}
#     analysis_type = 'invalid_type'
#     with pytest.raises(ValueError, match='The input analysis type has not been defined!'):
#         sleep_analysis_instance._execute([input_data, analysis_type])
