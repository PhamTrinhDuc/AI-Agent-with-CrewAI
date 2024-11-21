import json
import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew, Task
from pydantic import BaseModel
from typing import Union
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.2)

# Define output structure
class Output(BaseModel):
    explain: str
    example: str
    keyword: str

#Create an AI Agent
ai_expert_agent = Agent(
    role = "AI expert",
    goal = "Trả lời câu hỏi của người dùng về AI",
    backstory = "Bạn là một chuyên gia về AI."
    "Bạn hãy lắng nghe câu hỏi của người dùng và trả lời chi tiết kèm ví dụ minh họa",
    llm=llm
)

# Define a task
task = Task(
    description="Trả lời câu hỏi Machine Leaning là gì ?",
    expected_output="Một câu trả lời phù hợp với câu hỏi của người" 
    "lưu ý đưa ra ví dụ minh họa rõ ràng cho sự giải thích của mình",
    agent=ai_expert_agent,
    output_json=Output
)
# Initialize the Crew
crew = Crew(
    agents=[ai_expert_agent],
    tasks=[task],
    verbose=False
)

if __name__ == "__main__":
    # Run the Crew
    result = crew.kickoff()
    print(result)