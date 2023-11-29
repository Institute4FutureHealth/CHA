import pytest
from tasks.affect.sleep_get import SleepGet


@pytest.mark.parametrize("input_params, expected_output", [
    (['par_1', '2023-01-01', '2023-01-02'],
     '[{"date":1672531200000,"total_sleep_time":8.0,"awake_duration":0.33,'
     '"light_sleep_duration":5.0,"rem_sleep_duration":1.0,"deep_sleep_duration":1.67,'
     '"sleep_onset_latency":0.17,"midpoint_time_of_sleep":4.0,"sleep_efficiency":90,'
     '"average_heart_rate":70,"minimum_heart_rate":60,"rmssd":50,"average_breathing_rate":15,'
     '"temperature_variation":0.5},{"date":1672617600000,"total_sleep_time":7.5,'
     '"awake_duration":0.25,"light_sleep_duration":4.67,"rem_sleep_duration":1.17,'
     '"deep_sleep_duration":1.42,"sleep_onset_latency":0.25,"midpoint_time_of_sleep":3.75,'
     '"sleep_efficiency":85,"average_heart_rate":68,"minimum_heart_rate":55,"rmssd":48,'
     '"average_breathing_rate":14,"temperature_variation":0.6}]'),
])
def test_execute(input_params, expected_output):

    sleep_get_instance = SleepGet()

    result_json = sleep_get_instance._execute(input_params)

    assert result_json == expected_output
