from typing import Any, Dict
from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonAstREPLTool
from langchain_experimental.agents import create_csv_agent

# Load environment variables
load_dotenv()

# Initialize agents
def create_agents():
    # Instructions for the Python agent
    instructions = """
    You are an agent designed to write and execute Python code to answer questions.
    You have access to a Python REPL, which you can use to execute code.
    If you get an error, debug your code and try again.
    You have the 'qrcode' package installed.
    Always run the code to get the answer, even if you know it beforehand.
    If you cannot answer with code, return "I don't know".
    """
    
    # Base prompt
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)
    
    # Python agent
    python_tools = [PythonAstREPLTool()]
    python_agent = create_react_agent(
        prompt=prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"),
        tools=python_tools,
    )
    python_agent_executor = AgentExecutor(agent=python_agent, tools=python_tools, verbose=True)
    
    # CSV agent
    csv_agent_executor = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="data/episode_info.csv",
        verbose=True,
        allow_dangerous_code=True
    )
    
    # agent for languages.csv
    csv_agent_executor_languages = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="data/languages.csv",
        verbose=True,
        allow_dangerous_code=True
    )
    
    # agent for itjobs.csv
    csv_agent_executor_itjobs = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="data/it_jobs_2030.csv",
        verbose=True,
        allow_dangerous_code=True
    )
    
    # agent laptop_prices.csv
    csv_agent_executor_laptop_prices = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="data/laptop_prices.csv",
        verbose=True,
        allow_dangerous_code=True
    )
    
    csv_agent_executor_data_science = create_csv_agent(
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        path="data/data_science_job.csv",
        verbose=True,
        allow_dangerous_code=True
    )
    
    # Python agent wrapper
    def python_agent_executor_wrapper(original_prompt: str) -> Dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})
    
    # Tools for the grand agent
    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="Executes Python code based on natural language instructions. Does not accept code as input."
        ),
        Tool(
            name="CSV Agent episodes",
            func=csv_agent_executor.invoke,
            description="Answers questions using the data in data/episode_info.csv via pandas calculations."
        ),
        Tool(
            name="CSV Agent languages",
            func=csv_agent_executor_languages.invoke,
            description="Answers questions using the data in data/languages.csv via pandas calculations."
        ),
        Tool(
            name="CSV Agent it jobs",
            func=csv_agent_executor_itjobs.invoke,
            description="Answers questions using the data in data/it_jobs_2030.csv via pandas calculations."
        ),
        Tool(
            name="CSV Agent laptop prices",
            func=csv_agent_executor_laptop_prices.invoke,
            description="Answers questions using the data in data/laptop_prices.csv via pandas calculations."
        ),
        Tool(
            name="CSV Agent data science",
            func=csv_agent_executor_data_science.invoke,
            description="Answers questions using the data in data/data_science_job.csv via pandas calculations."
        )
    ]
    
    # Grand agent
    grand_agent_prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=grand_agent_prompt,
        llm=ChatOpenAI(temperature=0, model="gpt-4"),
        tools=tools,
    )
    grand_agent_executor = AgentExecutor(
        agent=grand_agent,
        tools=tools,
        verbose=True
    )
    
    return grand_agent_executor

# Function to invoke the agent
def handle_query(query: str) -> Dict[str, Any]:
    agent_executor = create_agents()
    response = agent_executor.invoke({"input": query})
    return response
