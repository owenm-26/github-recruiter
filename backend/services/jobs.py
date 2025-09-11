from .llm import *
from configs.logger import logger
from models.jobs import LanguagesList
from .exceptions import *


system_prompt = """
You're a job posting scraping API. Given a block of text, pull out relevant Computer Science languages and packages. 
You should treat frameworks and machine learning libraries as 'packages' while their underlying language should be considered 
the 'language'. 

Priority should be determined on the number of packages associated with that language as well as the number
of years of use or the proficiency with that language required.

The identifier for libraries should be the name one would find in a package.json or requirements.txt that is shorthand
for the package itself. Some examples of this are PyTorch -> torch and Python MongoDB -> pymongo.
"""

def parse_job_description(job_description: str):
    logger.info("Parsing a new job description...")

    agent = initialize_agent(sys_prompt=system_prompt, output_type=LanguagesList)
    if agent is None:
        raise AgentInitError("Failed to initialize agent")

    try:
        response = call_llm(agent=agent, prompt=f"Parse this: {job_description}")
        if not response:
            raise JobParseError("Empty response from LLM")
        return response
    except LLMCallError:
        raise
    except Exception as e:
        raise JobParseError(f"Unexpected error: {e}")