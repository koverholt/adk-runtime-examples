# adk-runtime-examples

Examples of running
[Agent Development Kit (ADK)](https://google.github.io/adk-docs/) agents
directly in Python.

## Overview

Most of the examples in the ADK documentation invoke the agents using external
tools such as `adk web`, which spins up a web UI for testing your agent in a
browser, `adk run`, which runs your agent on the command line, or
`adk api-server`, which spins up a FastAPI server that you can build other
applications on top of.

On the other hand, sometimes you want to run your AI agents directly in Python
scripts, batch jobs, notebooks, or UI frameworks. To help you get started in
this direction, this repository has example(s) of running AI agents using ADK
directly in Python, without the need to use external tooling or commands.

## Usage

1. Open a terminal and clone this repository:

    ```git clone https://github.com/koverholt/adk-runtime-examples.git```

2. Navigate to the directory with the Python script:

    ```cd adk-runtime-examples/adk-agent```

3. Define your `GOOGLE_API_KEY` from [Google AI Studio](https://aistudio.google.com/):

    ```export GOOGLE_API_KEY=AIzaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX```

4. Run the Python script:

    ```python agent.py```

5. You should see output similar to the following:

    ```
    $ python agent.py

    ** User says: What is the spaceflight news for today?

    --- Tool: get_spaceflight_news called for date: 2025-07-17 ---

    ** spaceflight_news_agent: Today in spaceflight news, several exciting
    developments have been reported. The final module for the Mobile Launcher 2
    (ML-2) tower, which will be used for the Artemis program's SLS Block 1B
    rocket, has been added. This is a significant step forward for future moon
    missions.

    In other news, The Exploration Company has successfully tested the Breeze
    thruster for its Nyx Moon lunar lander, a key milestone for the commercial
    space transportation startup. Also, new research from NASA and Oxford
    University has revealed that the planet Uranus is warmer than previously
    believed.

    Here are a few more top stories from today:

    * **NASA's X-59 Begins Taxi Tests:** The X-59 quiet supersonic aircraft has
        started its first taxi tests, moving under its own power for the first
        time. This is a crucial step towards demonstrating the ability to fly
        supersonic without creating a loud sonic boom.

    * **New Solar Mission:** NASA is preparing to launch the Solar EruptioN
        Integral Field Spectrograph (SNIFS) mission to study the Sun's
        chromosphere. The launch is scheduled for as early as July 18.

    * **Space Apps Challenge:** Registration is now open for the 2025 NASA
        International Space Apps Challenge, a global event that brings together
        people to solve challenges in space and on Earth.

    * **Robots for Planetary Exploration:** The European Space Agency (ESA) has
        been testing a four-legged robot in simulated microgravity conditions.
        This research is aimed at developing robots that can explore low-gravity
        environments like the Moon and Mars.
    ```
