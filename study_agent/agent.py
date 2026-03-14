from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    model="gemini-1.5-flash",
    name="study_agent",
    description="AI assistant for students learning programming and AI.",
    instruction="""
You are an AI mentor for students.
Explain technical topics clearly.
Give examples and simple explanations.
If the topic is programming, include sample code.
""",
)