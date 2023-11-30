# import json
# import pytest
# from tasks.affect.activity_analysis import ActivityAnalysis
# @pytest.fixture
# def activity_analysis_task():
#     return ActivityAnalysis()
# def test_execute_average_analysis(activity_analysis_task):
#     input_data = [
#         {"data": '{"date": ["2023-01-01"], "steps_count": [500], "rest_time": [360], "inactive_time": [180], '
#                  '"low_acitivity_time": [120], "medimum_acitivity_time": [60], "high_acitivity_time": [30]}'},
#         "average"
#     ]
#     result = activity_analysis_task._execute(input_data)
#     assert "steps_count" in result
#     assert "rest_time" in result
#     assert "inactive_time" in result
#     assert "low_acitivity_time" in result
#     assert "medimum_acitivity_time" in result
#     assert "high_acitivity_time" in result
# def test_execute_sum_analysis(activity_analysis_task):
#     input_data = [
#         {"data": '{"date": ["2023-01-01"], "steps_count": [500], "rest_time": [360], "inactive_time": [180], '
#                  '"low_acitivity_time": [120], "medimum_acitivity_time": [60], "high_acitivity_time": [30]}'},
#         "sum"
#     ]
#     result = activity_analysis_task._execute(input_data)
#     assert "steps_count" in result
#     assert "rest_time" in result
#     assert "inactive_time" in result
#     assert "low_acitivity_time" in result
#     assert "medimum_acitivity_time" in result
#     assert "high_acitivity_time" in result
# def test_execute_trend_analysis(activity_analysis_task):
#     input_data = [
#         {
#             "data": '{"date": ["2023-01-01"], "steps_count": [500], "rest_time": [360], "inactive_time": [180], '
#                     '"low_acitivity_time": [120], "medimum_acitivity_time": [60], "high_acitivity_time": [30]}'
#         },
#         "trend"
#     ]
#     result = activity_analysis_task._execute(input_data)
#     expected_result = [
#         {"steps_count": None, "rest_time": None, "inactive_time": None, "low_acitivity_time": None,
#          "medimum_acitivity_time": None, "high_acitivity_time": None}
#     ]
#     assert json.loads(result) == expected_result
