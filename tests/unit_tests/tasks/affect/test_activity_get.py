# from unittest import mock
# import pytest
# from unittest.mock import Mock, patch
# from tasks.affect.activity_get import ActivityGet
# import pandas as pd
# @pytest.fixture
# def activity_get_task():
#     return ActivityGet(name='affect_activity_get', chat_name='AffectActivityGet', description="Get the physical "
#                                                                                               "activity parameters...")
# @patch('tasks.affect.activity_get.os.path.join')
# @patch('tasks.affect.activity_get.ActivityGet._get_data')
# @patch('tasks.affect.activity_get.os.path.exists')
# def test_execute(mock_path_exists, mock_get_data, mock_os_path_join, activity_get_task):
#     mock_path_exists.return_value = True
#     mock_os_path_join.return_value = 'mocked_full_path'
#     expected_data = pd.DataFrame({
#         'date': ['2023-01-01'],
#         'steps': [500],
#         'rest': [360],
#         'inactive': [180],
#         'low': [120],
#         'medium': [60],
#         'high': [30]
#     })
#     mock_get_data.return_value = expected_data
#     result = activity_get_task._execute(["par_1", "2023-01-01", "2023-01-01"])
#     assert result == expected_data.to_json(orient='records')
