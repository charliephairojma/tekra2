from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain.llms import Ollama
from stock_analysis.tools.calculator_tool import CalculatorTool
from stock_analysis.tools.sec_tools import SEC10KTool, SEC10QTool
from stock_analysis.tools.pdf_tool import PDFTool
from stock_analysis.tools.email_tool import EmailTool
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool


ollama_llama3_1 = Ollama(model="llama3.1")


@CrewBase
class StockAnalysisCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def financial_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                # SEC10QTool("AMZN"),
                # SEC10KTool("AMZN"),
            ],
            llm=ollama_llama3_1
        )
    
    @task
    def financial_analysis(self) -> Task: 
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_agent(),
        )
    

    @agent
    def research_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['research_analyst'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                # WebsiteSearchTool(), 
                # SEC10QTool("AMZN"),
                # SEC10KTool("AMZN"),
            ],
            llm=ollama_llama3_1
        )
    
    @task
    def research(self) -> Task:
        return Task(
            config=self.tasks_config['research'],
            agent=self.research_analyst_agent(),
        )
    
    @agent
    def financial_analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                # SEC10QTool(),
                # SEC10KTool(),
            ],
            llm=ollama_llama3_1
        )
    
    @task
    def financial_analysis(self) -> Task: 
        return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_analyst_agent(),
        )
    
    @task
    def filings_analysis(self) -> Task:
        return Task(
            config=self.tasks_config['filings_analysis'],
            agent=self.financial_analyst_agent(),
        )

    @agent
    def investment_advisor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['investment_advisor'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
            ],
            llm=ollama_llama3_1
        )

    @task
    def recommend(self) -> Task:
        return Task(
            config=self.tasks_config['recommend'],
            agent=self.investment_advisor_agent(),
        )

    @agent
    def data_visualizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_visualizer'],
            verbose=True,
            tools=[
                CalculatorTool(),
            ],
            llm=ollama_llama3_1
        )

    @task
    def data_visualization(self) -> Task:
        return Task(
            config=self.tasks_config['data_visualization'],
            agent=self.data_visualizer_agent(),
        )

    @agent
    def web_developer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['web_developer'],
            verbose=True,
            tools=[
                # EmailTool(),
                PDFTool(),
            ],
            llm=ollama_llama3_1
        )

    @task
    def html_report_generation(self) -> Task:
        return Task(
            config=self.tasks_config['html_report_generation'],
            agent=self.web_developer_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Stock Analysis"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=2,
        )
