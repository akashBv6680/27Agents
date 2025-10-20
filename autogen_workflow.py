# autogen_workflow.py (AutoGen Workflow Orchestration - FINAL CORRECTED VERSION)
import os
from autogen import GroupChat, GroupChatManager
from autogen_config import *
from dotenv import load_dotenv

load_dotenv()

# --- 1. INITIAL SETUP ---

initial_task = "Initiate the 20-step AutoML pipeline. First, check the critical alert inbox, then proceed with data ingestion, comprehensive modeling, and finally, report the business impact and commit the final report."


# --- 2. Define Group Chat ---
autogen_group_chat = GroupChat(
    agents=agent_group,
    messages=[],
    max_round=50, 
    speaker_selection_method="auto"
)

# Manager uses the LLM_CONFIG that EXCLUDES tools
manager = GroupChatManager(
    groupchat=autogen_group_chat,
    llm_config=MANAGER_LLM_CONFIG,
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
