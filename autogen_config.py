# autogen_config.py (AutoGen Configuration - FINAL CORRECTED VERSION)
import os
from autogen import UserProxyAgent, AssistantAgent
from tools import email_checker, github_file_creator

# --- 1. LLM CONFIGURATIONS ---

# 1.1. LLM Config for AGENTS (Requires the 'tools' key to enable function calls)
LLM_CONFIG_MOCK = {
    "config_list": [
        {
            # Base LLM Connection (MOCK/LOCAL)
            "model": "mistral-7b-v0.2", 
            "api_key": "MOCK_API_KEY", 
            "base_url": "http://mock-llm-service:8080/v1" 
        }
    ],
    # This 'tools' list is REQUIRED for the agents (AutoGenToolAgent) to use the functions
    "tools": [
        email_checker.email_check_function,
        email_checker.data_processor_function,
        email_checker.email_communicator_function,
        github_file_creator.github_commit_function,
    ]
}

# 1.2. LLM Config for the MANAGER (MUST EXCLUDE the 'tools' key)
# The GroupChatManager only needs basic LLM access for speaker selection.
MANAGER_LLM_CONFIG = {
    "config_list": [
        {
            # Base LLM Connection (MOCK/LOCAL)
            "model": "mistral-7b-v0.2", 
            "api_key": "MOCK_API_KEY", 
            "base_url": "http://mock-llm-service:8080/v1" 
        }
    ],
    # Note: No "tools" key here, preventing the GroupChatManager ValueError.
}


# --- 2. AGENT DEFINITIONS (27+ Agents) ---

# --- System-Wide Tools Wrapper ---
class AutoGenToolAgent(AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # CRITICAL FIX: Define tools as a dictionary (name: function) for correct registration
        tool_functions = {
            "email_check_function": email_checker.email_check_function,
            "data_processor_function": email_checker.data_processor_function,
            "email_communicator_function": email_checker.email_communicator_function,
            "github_commit_function": github_file_creator.github_commit_function,
        }
        
        # Register the tools with the agent instance
        self.register_function(tool_functions)


# --- Project Management Team (Core Agents) ---
project_manager = UserProxyAgent(
    name="Executive_Project_Lead",
    system_message="Define project scope, ensure all dependencies are met, and manage the task flow. Your first action is to instruct the Critical_Alert_Monitor.",
    code_execution_config=False,
    human_input_mode="NEVER"
)

inbox_monitor = AutoGenToolAgent(
    name="Critical_Alert_Monitor",
    system_message="You are the first line of defense. Use the `email_check_function` tool to scan the IMAP inbox for critical alerts.",
    llm_config=LLM_CONFIG_MOCK
)

client_liaison = AutoGenToolAgent(
    name="Client_Communication_Strategist",
    system_message="Translate technical outcomes into simple, conversational English. Use the `email_communicator_function` tool to simulate sending the final report email.",
    llm_config=LLM_CONFIG_MOCK
)

# --- Data Acquisition Team (Core Agents) ---
data_ingestor = AutoGenToolAgent(
    name="Data_Ingestor_and_Analyzer",
    system_message="Use the `data_processor_function` tool with the 'download and analyze dataset' argument to determine the PROBLEM TYPE.",
    llm_config=LLM_CONFIG_MOCK
)

feature_engineer = AutoGenToolAgent(
    name="Feature_Engineer_and_Cleaner",
    system_message="Use the `data_processor_function` tool with the 'clean and feature' argument to simulate data preparation.",
    llm_config=LLM_CONFIG_MOCK
)

# --- Model Training Team (Core Agents) ---
training_coordinator = AutoGenToolAgent(
    name="Model_Training_Coordinator",
    system_message="You are responsible for the comprehensive AutoML process. Use the `data_processor_function` tool with the 'train all models' argument to simulate training and metric generation.",
    llm_config=LLM_CONFIG_MOCK
)

model_selector = AutoGenToolAgent(
    name="Model_Selector_and_Tuner",
    system_message="Analyze the raw training metrics and the problem type. Select the best model and determine the final business value based on the metrics. **Your final output must be the final report content in Markdown.**",
    llm_config=LLM_CONFIG_MOCK
)

# --- Deployment & Reporting Team (Core Agents) ---
reporter_git_manager = AutoGenToolAgent(
    name="Reporter_and_GitHub_Manager",
    system_message="Draft the final report and commit it. Use the `github_commit_function` tool with the Markdown content from the Model_Selector.",
    llm_config=LLM_CONFIG_MOCK
)

# --- Group the rest of the 27+ roles into a single specialized Assistant Agent for Autogen ---
specialized_automl_assistant = AssistantAgent(
    name="Specialized_AutoML_Assistant",
    system_message="You are the combined expertise of 20+ specialized agents (Auditors, Deployers, Validators, Tuners, all Trainers). You provide detailed, technical outputs.",
    llm_config=LLM_CONFIG_MOCK
)


# --- 3. AGENT GROUP ---
agent_group = [
    inbox_monitor, 
    data_ingestor, 
    feature_engineer, 
    training_coordinator,
    model_selector,
    reporter_git_manager,
    client_liaison,
    specialized_automl_assistant
]
