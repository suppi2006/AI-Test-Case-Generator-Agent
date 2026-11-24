
import json
import re

VALID_TYPES = ["Positive", "Negative", "Edge Case"]
VALID_PRIORITIES = ["High", "Medium", "Low"]


def extract_json(response):

    if isinstance(response, dict):
        return response

    response = str(response).strip()

    # Remove Markdown code fences
    response = re.sub(r"^```(?:json)?\s*", "", response)
    response = re.sub(r"\s*```$", "", response)

    # Extract JSON content
    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("AI did not return valid JSON.")

    try:
        return json.loads(response[start:end + 1])
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON response: {error}")


def validate_test_cases(response):

    data = extract_json(response)

    if not isinstance(data, dict):
        raise ValueError("Invalid response structure.")

    if "test_cases" not in data:
        raise ValueError("Test cases are missing.")

    test_cases = data["test_cases"]

    if not isinstance(test_cases, list) or not test_cases:
        raise ValueError("No test cases were generated.")

    required_fields = [
        "scenario_type",
        "title",
        "preconditions",
        "steps",
        "test_data",
        "expected_result",
        "priority"
    ]

    validated_cases = []

    for index, case in enumerate(test_cases, start=1):

        if not isinstance(case, dict):
            raise ValueError(f"Invalid test case at position {index}.")

        for field in required_fields:
            if field not in case or case[field] is None:
                raise ValueError(
                    f"Missing {field} in test case {index}."
                )

        # Validate text fields
        text_fields = [
            "scenario_type",
            "title",
            "preconditions",
            "expected_result",
            "priority"
        ]

        for field in text_fields:
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError(
                    f"Invalid {field} in test case {index}."
                )

        # Validate scenario type
        if case["scenario_type"] not in VALID_TYPES:
            raise ValueError(
                f"Invalid scenario type in test case {index}."
            )

        # Validate priority
        if case["priority"] not in VALID_PRIORITIES:
            raise ValueError(
                f"Invalid priority in test case {index}."
            )

        # Validate steps
        if (
            not isinstance(case["steps"], list)
            or not case["steps"]
            or not all(
                isinstance(step, str) and step.strip()
                for step in case["steps"]
            )
        ):
            raise ValueError(
                f"Invalid steps in test case {index}."
            )

        # Convert dictionary/list test data into readable text
        if isinstance(case["test_data"], (dict, list)):
            case["test_data"] = json.dumps(
                case["test_data"],
                ensure_ascii=False
            )

        elif isinstance(case["test_data"], str):
            if not case["test_data"].strip():
                raise ValueError(
                    f"Empty test data in test case {index}."
                )

        else:
            raise ValueError(
                f"Invalid test data in test case {index}."
            )

        # Assign unique test case ID
        case["test_case_id"] = f"TC-{index:03d}"

        validated_cases.append(case)

    data["test_cases"] = validated_cases

    return data
