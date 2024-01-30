from src.tasks.affect.ppg_get import PPGGet


def test_ppg_get_execute():
    patient_id = "par_5"
    start_date = "2020-08-01"
    end_date = "2020-08-30"
    ppg_get_task = PPGGet()

    result = ppg_get_task._execute([patient_id, start_date, end_date])
    print("result/////", result)
    assert isinstance(result, str)
