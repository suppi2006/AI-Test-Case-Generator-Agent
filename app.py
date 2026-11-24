
import streamlit as st
import pandas as pd

from agent import generate_cases

from database import (
    create_table,
    get_all_history,
    get_history_by_id,
    update_history,
    delete_history
)

from export_utils import test_cases_to_csv


# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="AI Test Case Generator",
    page_icon="🧪",
    layout="wide"
)

create_table()


# ----------------------------------
# CUSTOM CSS
# ----------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: 700;
    color: #2563eb;
}

.subtitle {
    font-size: 16px;
    color: #64748b;
}

div.stButton > button {
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------
# SESSION STATE
# ----------------------------------

if "active_history_id" not in st.session_state:
    st.session_state.active_history_id = None

if "editor_version" not in st.session_state:
    st.session_state.editor_version = 0


# ----------------------------------
# HELPER FUNCTIONS
# ----------------------------------

def convert_cases_to_dataframe(test_cases):

    rows = []

    for case in test_cases:
        steps = case.get("steps", [])

        if isinstance(steps, list):
            steps = "\n".join(steps)

        rows.append({
            "Test Case ID": case.get("test_case_id", ""),
            "Scenario Type": case.get("scenario_type", ""),
            "Title": case.get("title", ""),
            "Preconditions": case.get("preconditions", ""),
            "Steps": steps,
            "Test Data": case.get("test_data", ""),
            "Expected Result": case.get("expected_result", ""),
            "Priority": case.get("priority", "")
        })

    return pd.DataFrame(rows)


def convert_dataframe_to_cases(dataframe):

    test_cases = []

    for _, row in dataframe.iterrows():

        steps = str(row["Steps"]).splitlines()

        steps = [
            step.strip()
            for step in steps
            if step.strip()
        ]

        test_cases.append({
            "test_case_id": str(row["Test Case ID"]),
            "scenario_type": str(row["Scenario Type"]),
            "title": str(row["Title"]),
            "preconditions": str(row["Preconditions"]),
            "steps": steps,
            "test_data": str(row["Test Data"]),
            "expected_result": str(row["Expected Result"]),
            "priority": str(row["Priority"])
        })

    return test_cases


def display_test_cases(record, allow_edit=True):

    st.subheader("Generated Test Cases")

    st.write("**Feature:**", record.get("feature", ""))

    st.write(
        "**Testing Purpose:**",
        record.get("testing_purpose", "")
    )

    assumptions = record.get("assumptions", [])

    if assumptions:
        with st.expander("View Assumptions"):
            for assumption in assumptions:
                st.write("•", assumption)

    test_cases = record.get("test_cases", [])

    if not test_cases:
        st.warning("No test cases available.")
        return

    dataframe = convert_cases_to_dataframe(test_cases)

    # Display editable table
    if allow_edit:

        edited_dataframe = st.data_editor(
            dataframe,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key=f"editor_{record['id']}_{st.session_state.editor_version}"
        )

        st.caption(
            "You can edit the cells directly in the table."
        )

        # Download CSV
        csv_data = test_cases_to_csv(test_cases)

        st.download_button(
            label="⬇ Download Original CSV",
            data=csv_data,
            file_name=f"test_cases_{record['id']}.csv",
            mime="text/csv"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save Edited Test Cases",
                key=f"save_{record['id']}"
            ):

                updated_cases = convert_dataframe_to_cases(
                    edited_dataframe
                )

                updated_result = {
                    "feature": record.get("feature", ""),
                    "testing_purpose": record.get(
                        "testing_purpose", ""
                    ),
                    "assumptions": assumptions,
                    "test_cases": updated_cases
                }

                update_history(
                    record["id"],
                    updated_result
                )

                st.session_state.editor_version += 1

                st.success("Changes saved successfully!")
                st.rerun()

        with col2:

            case_ids = [
                case.get("test_case_id")
                for case in test_cases
            ]

            selected_ids = st.multiselect(
                "Select test cases to delete",
                options=case_ids,
                key=f"delete_select_{record['id']}"
            )

            if st.button(
                "🗑 Delete Selected Test Cases",
                key=f"delete_cases_{record['id']}"
            ):

                if not selected_ids:
                    st.warning("Select at least one test case.")

                else:

                    remaining_cases = [
                        case for case in test_cases
                        if case.get("test_case_id") not in selected_ids
                    ]

                    updated_result = {
                        "feature": record.get("feature", ""),
                        "testing_purpose": record.get(
                            "testing_purpose", ""
                        ),
                        "assumptions": assumptions,
                        "test_cases": remaining_cases
                    }

                    update_history(
                        record["id"],
                        updated_result
                    )

                    st.session_state.editor_version += 1

                    st.success("Selected test cases deleted!")
                    st.rerun()

    else:

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True
        )


# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("🧪 AI Test Generator")

st.sidebar.write(
    "Generate and manage software test cases using AI."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Generate Test Cases",
        "History",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "Powered by Python, Streamlit, LangChain and Ollama"
)


# ----------------------------------
# PAGE 1: GENERATE TEST CASES
# ----------------------------------

if page == "Generate Test Cases":

    st.markdown(
        '<p class="main-title">AI Test Case Generator</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">'
        'Convert software requirements into structured test cases '
        'using a local AI model.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Enter Software Requirement")

    requirement = st.text_area(
        "Describe the feature or functionality:",
        placeholder=(
            "Example: A user should be able to log in "
            "using email and password."
        ),
        height=150
    )

    if st.button(
        "🚀 Generate Test Cases",
        type="primary",
        use_container_width=True
    ):

        if not requirement.strip():

            st.warning(
                "Please enter a software requirement."
            )

        elif len(requirement.strip()) < 10:

            st.warning(
                "Please enter a clear and meaningful requirement."
            )

        else:

            try:

                with st.spinner(
                    "AI is analyzing the requirement and generating test cases..."
                ):

                    result = generate_cases(requirement)

                history = get_all_history()

                st.session_state.active_history_id = history[0]["id"]

                st.success(
                    f"Successfully generated {len(result['test_cases'])} test cases!"
                )

                st.rerun()

            except Exception as error:

                st.error(
                    "Unable to generate test cases."
                )

                st.exception(error)

    # Show most recently generated test cases
    if st.session_state.active_history_id is not None:

        record = get_history_by_id(
            st.session_state.active_history_id
        )

        if record:

            st.divider()

            st.write("**Requirement:**")
            st.info(record["requirement"])

            display_test_cases(record)


# ----------------------------------
# PAGE 2: HISTORY
# ----------------------------------

elif page == "History":

    st.title("📚 Test Case History")

    st.write(
        "View previously generated and saved test cases."
    )

    history = get_all_history()

    if not history:

        st.info("No saved history available yet.")

    else:

        history_options = {
            f"#{item['id']} - {item['requirement'][:65]} "
            f"({item['created_at']})": item["id"]
            for item in history
        }

        selected_label = st.selectbox(
            "Select a saved requirement",
            list(history_options.keys())
        )

        selected_id = history_options[selected_label]

        record = get_history_by_id(selected_id)

        if record:

            st.divider()

            st.write("**Requirement:**")
            st.info(record["requirement"])

            st.write(
                "**Created At:**",
                record["created_at"]
            )

            display_test_cases(record)

            st.divider()

            if st.button(
                "🗑 Delete Entire History Record",
                type="secondary"
            ):

                delete_history(selected_id)

                if st.session_state.active_history_id == selected_id:
                    st.session_state.active_history_id = None

                st.success("History record deleted successfully!")

                st.rerun()


# ----------------------------------
# PAGE 3: ABOUT
# ----------------------------------

elif page == "About":

    st.title("About AI Test Case Generator")

    st.write("""
    AI Test Case Generator is an intelligent application
    that converts software requirements into structured
    software test cases.

    ### Technologies Used

    - Python – Core programming language
    - Streamlit – User interface
    - Ollama – Local Large Language Model
    - Llama 3.2 – AI model
    - LangChain – Prompt and model integration
    - SQLite – Database and history storage
    - Pandas – Tabular data processing

    ### Main Features

    - Automatic test case generation
    - Positive scenario identification
    - Negative scenario identification
    - Edge case identification
    - JSON response validation
    - Editable test case table
    - Delete individual test cases
    - Save and retrieve history
    - CSV export
    - Local AI processing

    ### Workflow

    Software Requirement
            ↓
    AI Requirement Analysis
            ↓
    Scenario Identification
            ↓
    Test Case Generation
            ↓
    JSON Validation
            ↓
    SQLite Storage
            ↓
    Review, Edit and Export
    """)
