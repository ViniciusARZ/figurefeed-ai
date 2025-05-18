import os
from crewai import Agent, Crew, Task, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from typing import List
import yaml
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class FigureCaptionCrew:
    def __init__(self, caption_model: str, api_key: str, verbose: bool = False) -> None:
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.agents_config = os.path.join(self.base_dir, "config", "agents.yaml")
        self.tasks_config = os.path.join(self.base_dir, "config", "tasks.yaml")

        self.caption_llm = LLM(model=caption_model, api_key=api_key)
        self.verbose = verbose

        # Initialize agents
        self._figure_researcher = self.figure_researcher()
        self._caption_generator = self.caption_generator()

        # Initialize tasks
        self._research_task = self.research_task()
        self._caption_task = self.caption_task()

        self.agents = [self._figure_researcher, self._caption_generator]
        self.tasks = [self._research_task, self._caption_task]

    @agent
    def figure_researcher(self) -> Agent:
        with open(self.agents_config, encoding="utf=8") as f:
            config = yaml.safe_load(f)
        return Agent(
            config=config["figure_researcher"],
            llm=self.caption_llm,
            verbose=self.verbose
        )

    @agent
    def caption_generator(self) -> Agent:
        with open(self.agents_config, encoding="utf=8") as f:
            config = yaml.safe_load(f)
        return Agent(
            config=config["caption_formatter"],
            llm=self.caption_llm,
            verbose=self.verbose
        )

    @task
    def research_task(self) -> Task:
        with open(self.tasks_config, encoding="utf-8") as f:
            config = yaml.safe_load(f)
        return Task(
            config=config["research_task"],
            agent=self._figure_researcher
        )

    @task
    def caption_task(self) -> Task:
        with open(self.tasks_config, encoding="utf-8") as f:
            config = yaml.safe_load(f)

        return Task(
            config=config["caption_task"],
            agent=self._caption_generator,
            input_keys=["result"]
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=self.verbose
        )