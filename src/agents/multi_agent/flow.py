from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langgraph_swarm import SwarmState, create_handoff_tool, add_active_agent_router
from src.config.llm import llm_2_5_flash_preview
from .tools import retrieve_document, send_gmail
from .prompt import admission_consultant_prompt, career_consultant_prompt
from langgraph.checkpoint.memory import InMemorySaver

# Handoffs

admission_consultant_name = "admission_consultant"
career_consultant_name = "career_consultant"

# Define agents
admission_consultant_assistant = create_react_agent(
    model=llm_2_5_flash_preview,
    tools=[
        retrieve_document,
        send_gmail,
        create_handoff_tool(
            agent_name=career_consultant_name,
        ),
    ],
    prompt=admission_consultant_prompt,
    name=admission_consultant_name,
)
career_consultant_assistant = create_react_agent(
    model=llm_2_5_flash_preview,
    tools=[
        create_handoff_tool(
            agent_name=admission_consultant_name,
        ),
    ],
    prompt=career_consultant_prompt,
    name=career_consultant_name,
)

checkpointer = InMemorySaver()
workflow = (
    StateGraph(SwarmState)
    .add_node(
        admission_consultant_assistant, destinations=(str(career_consultant_name),)
    )
    .add_node(
        career_consultant_assistant, destinations=(str(admission_consultant_name),)
    )
)
workflow = add_active_agent_router(
    builder=workflow,
    route_to=[str(admission_consultant_name), str(career_consultant_name)],
    default_active_agent=str(admission_consultant_name),
)

app = workflow.compile(checkpointer=checkpointer)