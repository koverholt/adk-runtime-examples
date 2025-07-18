import asyncio
import datetime
import requests
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

# Define constants
APP_NAME = "spaceflight-news"
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
    return response.json()

# Define today's date for later usage in prompt template
TODAY = str(datetime.datetime.now().isoformat())

# Agent definition
spaceflight_news_agent = Agent(
    name="spaceflight_news_agent",
    model=MODEL_ID,
    description="Provides space flight news information for a given date.",
    instruction="You are a helpful space flight news assistant."
                "Use the tool 'get_spaceflight_news' to retrieve space flight news."
                "If the user gives an ambiguous date, assume a specific date."
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the space flight news"
                "clearly with a summary of only a few sentences."
                f"Today's date is: {TODAY}",
    tools=[get_spaceflight_news],
)

# Define the agent runner
runner = InMemoryRunner(
    agent=spaceflight_news_agent,
    app_name=APP_NAME,
)

# Create a session for our agent
def create_session():
    session = asyncio.run(
        runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    ))
    return session

print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# Define a convenience function to query the agent
def query_agent(prompt: str, session_id: str):
    print("** User:", prompt)
    response = runner.run(new_message=types.Content(
            role="user",
            parts=[types.Part(text=prompt)]), user_id=USER_ID, session_id=session_id)
    for message in response:
        if message.content.parts and message.content.parts[0].text:
            print(f'** {message.author}: {message.content.parts[0].text}')
            print()

# Define sample prompts to use when the script is run
session = create_session()
query_agent("Hello!", session_id=session.id)
query_agent("What is the spaceflight news for today?", session_id=session.id)
query_agent("What is the spaceflight news as of Jan 2022?", session_id=session.id)
query_agent("What is the spaceflight news as of Jan 1900?", session_id=session.id)
