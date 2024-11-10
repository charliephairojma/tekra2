from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain.llms import Ollama, OpenAI
from langchain_openai import ChatOpenAI

from stock_analysis.tools.calculator_tool import CalculatorTool
from stock_analysis.tools.sec_tools import SEC10KTool, SEC10QTool
from stock_analysis.tools.pdf_tool import PDFTool
from stock_analysis.tools.email_tool import EmailTool
# from stock_analysis.tools.vector_db_tool import VectorDBTool
from crewai_tools import (
	WebsiteSearchTool, 
	ScrapeWebsiteTool
)

ollama_llama3_1 = Ollama(model="llama3.1")

chat_gpt_4o_mini = ChatOpenAI(model="gpt-4o-mini")

@CrewBase
class StockAnalysisCrew:
	agents_config = 'config/agents2.yaml'
	tasks_config = 'config/tasks2.yaml'
	
	@agent
	def investment_manager_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['investment_manager'],
			llm=chat_gpt_4o_mini,
			max_iter=3,
			max_rpm=10,
			tools=[
				ScrapeWebsiteTool(),
				WebsiteSearchTool(),
				CalculatorTool(),
				SEC10QTool(),
				SEC10KTool(),
				# VectorDBTool()
			]
			)
	
	@agent
	def financial_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['financial_analyst'],
			llm=chat_gpt_4o_mini,
			max_iter=3,
			max_rpm=10,
			tools=[
				ScrapeWebsiteTool(),
				WebsiteSearchTool(),
				CalculatorTool(),
				SEC10QTool(),
				SEC10KTool(),
				# VectorDBTool()
			]
			)
	
	@agent
	def research_analyst_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['market_research_analyst'],
			llm=chat_gpt_4o_mini,
			max_iter=3,
			max_rpm=10,
			tools=[
				ScrapeWebsiteTool(),
				WebsiteSearchTool(),
				# VectorDBTool()
			]
			)
	
	@agent
	def financial_visualizer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['data_visualization_specialist'],
			llm=chat_gpt_4o_mini,
			max_iter=3,
			tools=[
				CalculatorTool()
			]
			)

	@agent
	def web_developer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['report_writer'],
			llm=chat_gpt_4o_mini,
			max_iter=3,
			tools=[
				PDFTool(),
				EmailTool()
			]
			)

	@task
	def financial_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['financial_analysis'],
			agent=self.financial_analyst_agent()
			)

	@task
	def research(self) -> Task:
		return Task(
			config=self.tasks_config['market_research'],
			agent=self.research_analyst_agent()
			)

	@task
	def filings_analysis(self) -> Task:
		return Task(
			config=self.tasks_config['sec_filings_analysis'],
			agent=self.financial_analyst_agent()
			)

	@task
	def html_report(self) -> Task:
		return Task(
			config=self.tasks_config['html_report_generation'],
			agent=self.web_developer_agent()
			)

	@task
	def recommend(self) -> Task:
		return Task(
			config=self.tasks_config['investment_recommendation'],
			agent=self.investment_manager_agent()
			)

	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=[
				self.investment_manager_agent(),
				self.financial_analyst_agent(),
				self.research_analyst_agent(),
				self.financial_visualizer_agent(),
				self.web_developer_agent()
			],
			tasks=[
				self.financial_analysis(),
				self.research(),
				self.filings_analysis(),
				self.html_report(),
				self.recommend()
			],
			process=Process.sequential
		)