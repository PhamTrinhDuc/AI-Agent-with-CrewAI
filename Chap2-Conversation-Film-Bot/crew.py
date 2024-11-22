from crewai import Crew, Agent, Task, Process
from crewai.project import CrewBase, agent, task, crew
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

@CrewBase
class CrewaiFilmChatbotCrew:
    pass