# AI Test Case Generator Agent

An AI-powered application that automatically generates structured software test cases from plain-English requirements using a locally running Large Language Model (LLM).

## Project Overview

The AI Test Case Generator Agent helps software testers and developers reduce the time required to write manual test cases.

Users can enter a software requirement, and the application analyzes it to generate relevant Positive, Negative, and Edge Case scenarios with test steps, test data, expected results, and priority levels.

The generated test cases can be reviewed, edited, deleted, saved, and exported as CSV files.

## Features

- **Requirement Analysis:** Understands software requirements written in natural language.
- **AI Test Case Generation:** Generates structured test cases using a local LLM.
- **Scenario Classification:** Identifies Positive, Negative, and Edge Case scenarios.
- **Detailed Test Cases:** Provides test case ID, title, preconditions, steps, test data, expected result, and priority.
- **Priority Assignment:** Assigns High, Medium, or Low priority.
- **Edit and Delete:** Allows users to modify or remove generated test cases.
- **History Management:** Stores previous test case generations using SQLite.
- **CSV Export:** Downloads test cases in CSV format.
- **Input Validation:** Handles empty requirements and invalid AI responses.
- **Local AI Processing:** Uses Ollama to run the language model locally.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web application interface |
| Ollama | Running local LLM |
| Llama 3.2 (3B) | Test case generation |
| LangChain | LLM integration and prompt management |
| SQLite | Storing test case history |
| Pandas | Data handling and CSV export |

## System Workflow

1. User enters a software requirement.
2. The agent analyzes the requirement.
3. A structured prompt is prepared using LangChain.
4. Ollama processes the prompt using the local Llama 3.2 model.
5. The model generates test cases in JSON format.
6. Python validates the generated response.
7. Test cases are displayed in the Streamlit application.
8. Users can edit, delete, and save test cases.
9. Generated results are stored in SQLite.
10. Users can download the final test cases as CSV.

## Project Structure

```text
AI-Test-Case-Generator-Agent/
│
├── app.py
├── agent.py
├── prompts.py
├── test_case_generator.py
├── database.py
├── export_utils.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── test_cases.db
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Test-Case-Generator-Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and Run Ollama

Download Ollama from:

https://ollama.com/

Pull the required model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running before starting the application.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

## Sample Input

```text
A user should be able to log in using
a registered email address and password.
```

## Expected Output

The application generates test cases covering scenarios such as:

- Valid login credentials
- Invalid email address
- Incorrect password
- Empty input fields
- Other relevant boundary and edge scenarios

Each test case includes steps, test data, expected results, and priority.

## Database

SQLite is used to store generated test case history.

The application allows users to access previously generated test cases even after restarting the application.

## Testing

The application was tested for:

- Valid software requirements
- Test case generation
- Editing and deleting test cases
- Saving generated results
- Viewing previous history
- CSV export
- Empty input validation
- History persistence after application restart

## Future Enhancements

- Improve test case generation accuracy.
- Support additional local language models.
- Add test case generation for different software modules.
- Provide PDF and Excel export options.
- Add automated test script generation.

## Learning Outcomes

Through this project, I gained practical experience in:

- Building AI-powered applications using Python.
- Working with locally hosted Large Language Models.
- Integrating LangChain with Ollama.
- Designing structured prompts.
- Validating AI-generated JSON responses.
- Managing application data using SQLite.
- Developing interactive applications using Streamlit.

## Author

**Rasi Supriya**

GitHub: https://github.com/suppi2006

---

*This project was developed as part of an AI Engineering learning project.*