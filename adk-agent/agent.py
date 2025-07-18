import asyncio
import datetime
import requests
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

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
    model="gemini-2.5-pro",
    description="Provides space flight news information for a given date.",
    instruction="You are a helpful space flight news assistant."
                "If the user gives a partial date, assume a specific date."
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the space flight news"
                "clearly with a summary of a few sentences."
                f"Today's date is: {TODAY}",
    tools=[get_spaceflight_news],
)

# Agent runner
runner = InMemoryRunner(
    agent=spaceflight_news_agent,
    app_name='my_app',
)

# Create a session for our agent
def create_session():
    session = asyncio.run(runner.session_service.create_session(
        app_name='my_app', user_id='user'
    ))
    return session

# Define a convenience function to query the agent
def run_agent(session_id: str, new_message: str):
    content = types.Content(
        role='user', parts=[types.Part.from_text(text=new_message)]
    )
    print('** User says:', new_message)
    for event in runner.run(
        user_id='user',
        session_id=session_id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(f'** {event.author}: {event.content.parts[0].text}')
    print()

# Define sample prompts to use when the script is run
if __name__ == '__main__':
    session = create_session()
    run_agent(session.id, "Hello!")
    run_agent(session.id, "What is the spaceflight news for today?")
    run_agent(session.id, "What is the spaceflight news as of Jan 2022?")
    run_agent(session.id, "What is the spaceflight news as of Jan 1900?")
