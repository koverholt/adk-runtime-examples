import datetime
import requests
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Define constants
APP_NAME = "weather"
USER_ID = "user"
SESSION_ID = "session"
MODEL_ID = "gemini-2.5-pro"

# Define a tool for agent to use to get space flight news
def get_spaceflight_news(date: str) -> dict:
    """
    Retrieves spaceflight news for a given date.

    Args:
        date (str): The date (ISO 8601 date format)
    """
    print(f"--- Tool: get_spaceflight_news called for date: {date} ---")
    response = requests.get("https://api.spaceflightnewsapi.net/v4/articles/")
    print(type(response.json()))
    return response.json()

# Define today's date for later usage in prompt template
TODAY = str(datetime.datetime.now().isoformat())

# Agent definition
spaceflight_news_agent = Agent(
    name="spaceflight_news_agent",
    model=MODEL_ID,
    description="Provides space flight news information for a given date.",
    instruction="You are a helpful space flight news assistant."
                "Use the tool 'get_spaceflight_news' to retrieve space flight news"
                "If the user gives a partial date, assume a specific date."
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the space flight news"
                "clearly with a summary of a few sentences."
                f"Today's date is: {TODAY}",
    tools=[get_spaceflight_news],
)

session_service = InMemorySessionService()

session = session_service.create_session_sync(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

runner = Runner(
    agent=spaceflight_news_agent,
    app_name=APP_NAME,
    session_service=session_service
)

print(f"Runner created for agent '{runner.agent.name}'.")

def query_agent(prompt: str):
    print("User input:", prompt)
    response = runner.run(new_message=types.Content(
            role="user",
            parts=[types.Part(text=prompt)]), user_id="user", session_id="session")
    import time
    time.sleep(10)
    for message in response:
        agent_output = message.content
        print("Agent output:", agent_output)
        print()
        return agent_output

# Define sample prompts to use when the script is run
query_agent("Hello!")
query_agent("What is the spaceflight news for today?")
query_agent("What is the spaceflight news as of Jan 2022?")
query_agent("What is the spaceflight news as of Jan 1900?")
