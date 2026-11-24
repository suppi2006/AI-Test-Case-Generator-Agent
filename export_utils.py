
import pandas as pd


def test_cases_to_csv(test_cases):

    rows = []

    for case in test_cases:
        rows.append({
            "Test Case ID": case.get("test_case_id", ""),
            "Scenario Type": case.get("scenario_type", ""),
            "Title": case.get("title", ""),
            "Preconditions": case.get("preconditions", ""),
            "Steps": "\n".join(case.get("steps", [])),
            "Test Data": case.get("test_data", ""),
            "Expected Result": case.get("expected_result", ""),
            "Priority": case.get("priority", "")
        })

    dataframe = pd.DataFrame(rows)

    return dataframe.to_csv(index=False).encode("utf-8-sig")
