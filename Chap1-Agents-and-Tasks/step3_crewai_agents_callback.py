import json
import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Crew, Task
from crewai.tasks.task_output import TaskOutput
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1.2)

def callback_func(output: TaskOutput):
    # Do something after the task is completed
    # Example: Send an email to the manager
    print(f"""
        Task completed !
        Task: {output.description}
        Output: {output.raw}
    """)


llm = ChatOpenAI(model="gpt-4o-mini")
class StructuredOutput(BaseModel):
    explain: str
    example: str
    keyword: str


# Create AI Research Agents
agent_research = Agent(
    role = "Chuyên gia về AI",
    goal = "Hỗ trợ giải đáp các câu hỏi về AI",
    backstory = "Bạn là 1 chuyên gia trong lĩnh vực AI. Hãy lắng nghe các câu hỏi của người dùng và trả lời 1 cách phù hợp",
    llm=llm,
    verbose = False
)

# Create Blog AI Agent
agent_blog = Agent(
    role="Chuyên giá viết blog",
    goal="Viết 1 bài blog chất lượng về AI",
    backstory="Bạn là 1 chuyên gia viết blog về AI, luôn sẵn sàng tiếp nhận và chỉnh sửa bài viết theo nhận xét",
    llm = llm,
    verbose=False
)

# Define Tasks Generate Keywords
keywork_task  = Task(
    name="Search keyword",
    description="Đưa ra những keyword qua trọng về chủ đề Machine learning",
    expected_output="Một danh sách các từ khóa quan trọng về Machine Learning",
    agent=agent_research,
    output_json=StructuredOutput,
    callback=callback_func,
)

# Define task Create Blog Outline
outline_task = Task(
    name = "write outline blog",
    description="Đưa ra dàn ý phù hợp cho bài viết về chủ đề Machine Learning",
    agent=agent_research,
    expected_output="Một mô tả chi tiết về bài viết",
    output_json=StructuredOutput,
    callback=callback_func
)

# Define Task Write Blog Content
write_task = Task(
    name="write blog task",
    description="Viết nội dung cho bài viết về chủ đề Machine Learning khoảng",
    expected_output="Một bài viết chất lượng khoảng 200 từ",
    agent=agent_blog, 
    context=[keywork_task, outline_task],
    output_json=StructuredOutput,
    callback=callback_func
)

# Define Crew
crew = Crew(
    agents=[agent_research, agent_blog],
    tasks=[keywork_task, outline_task, write_task],
    verbose=False,
    output_json=StructuredOutput
)

if __name__ == "__main__":
    results = crew.kickoff()
    print(results)