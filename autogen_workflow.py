# autogen_workflow.py (AutoGen Workflow Orchestration)
import os
from autogen import GroupChat, GroupChatManager
from autogen_config import *
from dotenv import load_dotenv

load_dotenv()

# --- 1. INITIAL SETUP ---

initial_task = "Initiate the 20-step AutoML pipeline. First, check the critical alert inbox, then proceed with data ingestion, comprehensive modeling, and finally, report the business impact and commit the final report."


# --- 2. Define Group Chat ---
# AutoGen handles the complex task graph (your 20 tasks) through conversation.
# The manager decides who speaks next based on the task state.
autogen_group_chat = GroupChat(
    agents=agent_group,
    messages=[],
    max_round=50, # Allow ample time for the conversation to complete the full 20-step task
    speaker_selection_method="auto"
)

manager = GroupChatManager(
    groupchat=autogen_group_chat,
    llm_config=LLM_CONFIG_MOCK,
    is_termination_msg=lambda x: "SUCCESS: Email successfully composed and SIMULATED" in x.get("content", "")
)

# --- 3. Run the Workflow ---
if __name__ == "__main__":
    print(f"--- 🚀 Starting Autonomous Data Scientist Crew (AutoGen) ---")
    
    # The Executive_Project_Lead initiates the conversation with the task
    project_manager.initiate_chat(
        manager,
        message=initial_task,
    )
    
    print("\n\n################################################")
    print("### AUTOGEN WORKFLOW COMPLETE (AutoML Pipeline) ###")
    print("################################################")
