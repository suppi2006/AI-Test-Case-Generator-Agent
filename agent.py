
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from prompts import SYSTEM_PROMPT
from test_case_generator import validate_test_cases
from database import create_table, save_test_cases


class TestCaseAgent:

    def __init__(self):

        # Connect to the local Ollama model
        self.llm = ChatOllama(
            model="llama3.2:3b",
            temperature=0.1,
            format="json"
        )

        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "Analyze this software requirement:\n{requirement}")
        ])

        # Connect prompt and AI model
        self.chain = self.prompt | self.llm

    def generate_test_cases(self, requirement):

        # Validate empty input
        if not requirement or not requirement.strip():
            raise ValueError("Please enter a software requirement.")

        # Ask AI to analyze and generate test cases
        response = self.chain.invoke({
            "requirement": requirement.strip()
        })

        # Validate the AI response
        result = validate_test_cases(response.content)

        return result


def generate_cases(requirement):

    # Create database table if it does not exist
    create_table()

    # Initialize AI agent
    agent = TestCaseAgent()

    # Generate and validate test cases
    result = agent.generate_test_cases(requirement)

    # Save generated test cases into SQLite
    save_test_cases(requirement.strip(), result)

    return result
