from crewai import Agent, Task, Crew, LLM
from crewai.crew import CrewOutput
from crewai_tools import NL2SQLTool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".env")

class DatabaseCrew:
    def __init__(self, nl2sqltool: NL2SQLTool, llm: LLM):
        self.nl2sqltool = nl2sqltool
        self.llm = llm
    
    def database_agent(self) -> Agent:
        return Agent(
            role="SQL Specialist",
            goal="Execute SQL queries to retrieve relevant data from the database.",
            backstory="You are a database and SQL query specialist, capable of transforming requests into precise and efficient queries.",
            tools=[self.nl2sqltool],
            llm=self.llm,
            verbose=True
        ) 

    def database_query(self) -> Task:
        return Task(
            name="DatabaseQuery",
            description="""
                Answer the following question querying the database: {question}.
                To respond the question, identify the user goal and execute SQL queries against the database.
                Tools:
                Use 'NL2SQLTool' to convert natural language to SQL.""",       
            expected_output=(
                "The answer for the user in a markdown file. The file should contain the user's question and below it the answer you generated."
                "Example answer:"
                "# User Question:"
                "- How many albums are in the database?"
                "# Response:"
                "- There are 17 albums."
            ),
            agent=self.database_agent(),
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.database_agent()],
            tasks=[self.database_query()],
            verbose=True
        )
    
    @staticmethod
    def append_response_file(output_path: str, crew_output_raw: str) -> None:
        with open(output_path, mode="a", encoding="utf-8") as file:
            file.write(f"{crew_output_raw}\n\n---\n\n")

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

DB_URI = "sqlite:///chinook.db"
nl2sql = NL2SQLTool(db_uri=DB_URI)

api_key = {
    "gemini_api_key": os.environ.get("GEMINI_API_KEY"),
    "open_ai_api_key": os.environ.get("OPEN_API_KEY")
}
model = {
    "gpt-4.1-mini": "openai/gpt-4.1-mini",
    "gemini-2.0-flash": "gemini/gemini-2.0-flash"
}
llm: LLM = LLM(
    model=model.get("gpt-4.1-mini"),
    api_key=api_key.get("openai_api_key"),
    temperature=0.2
)

db_crew = DatabaseCrew(nl2sqltool=nl2sql, llm=llm).crew()
question = input("Enter your question for the agent: ")
crew_output: CrewOutput = db_crew.kickoff(inputs={
    "question": question
})

output_path = os.path.join(OUTPUT_DIR, "responses.md")
DatabaseCrew.append_response_file(output_path, crew_output.raw)