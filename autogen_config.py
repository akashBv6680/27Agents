# autogen_config.py (AutoGen Configuration - FINAL)
import os
from autogen import UserProxyAgent, AssistantAgent
from tools import email_checker, github_file_creator

# --- 1. LLM CONFIGURATION (MOCK/TEMPLATE) ---
# Since we removed Ollama, we use a mock config. 
# You can replace this with your actual local or cloud LLM endpoint.
# For local LLM via AutoGen, you'd use a different BASE_URL.
LLM_CONFIG_MOCK = {
    "config_list": [
        {
            # You can change this to a local endpoint if Ollama is running separately
            "model": "mistral-7b-v0.2", 
            "api_key": "MOCK_API_KEY", 
            "base_url": "http://mock-llm-service:8080/v1" 
        }
    ],
    # Add tools to the LLM configuration so agents can access them
    "tools": [
        email_checker.email_check_function,
        email_checker.data_processor_function,
        email_checker.email_communicator_function,
        github_file_creator.github_commit_function,
    ]
}

# --- 2. AGENT DEFINITIONS (27+ Agents) ---

# --- System-Wide Tools Wrapper ---
class AutoGenToolAgent(AssistantAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # CRITICAL FIX: Define tools as a dictionary (name: function) before registering
        tool_functions = {
            "email_check_function": email_checker.email_check_function,
            "data_processor_function": email_checker.data_processor_function,
            "email_communicator_function": email_checker.email_communicator_function,
            "github_commit_function": github_file_creator.github_commit_function,
            # We will wrap the read_knowledge_tool logic directly into the agents' prompts
        }
        
        # Register the tools using the dictionary, resolving the AttributeError
        self.register_function(tool_functions)


# --- Project Management Team (5 Agents) ---
project_manager = UserProxyAgent(
    name="Executive_Project_Lead",
    # The 'UserProxyAgent' acts as the initiator and code executor (if code_execution_config=True)
    system_message="Define project scope, ensure all dependencies are met, and manage the task flow. Your first action is to instruct the Inbox_Monitor.",
    code_execution_config=False, # Project Manager does not execute code
    human_input_mode="NEVER"
)

inbox_monitor = AutoGenToolAgent(
    name="Critical_Alert_Monitor",
    system_message="You are the first line of defense. Use the `email_check_function` tool to scan the IMAP inbox for critical alerts with keywords like 'model drift', 'production error', or 'sales crash'.",
    llm_config=LLM_CONFIG_MOCK
)

client_liaison = AutoGenToolAgent(
    name="Client_Communication_Strategist",
    system_message="Translate technical outcomes into simple, conversational English. Use the `email_communicator_function` tool to simulate sending the final report email.",
    llm_config=LLM_CONFIG_MOCK
)

# --- Data Acquisition Team (Core 2 Agents) ---
data_ingestor = AutoGenToolAgent(
    name="Data_Ingestor_and_Analyzer",
    system_message="Use the `data_processor_function` tool with the 'download and analyze dataset' argument to determine the PROBLEM TYPE (Regression, Classification, or Clustering).",
    llm_config=LLM_CONFIG_MOCK
)

feature_engineer = AutoGenToolAgent(
    name="Feature_Engineer_and_Cleaner",
    system_message="Use the `data_processor_function` tool with the 'clean and feature' argument to simulate data preparation and feature engineering.",
    llm_config=LLM_CONFIG_MOCK
)

# --- Model Training Team (Core 2 Agents) ---
training_coordinator = AutoGenToolAgent(
    name="Model_Training_Coordinator",
    system_message="You are responsible for the comprehensive AutoML process. Use the `data_processor_function` tool with the 'train all models' argument to simulate the full training and metric generation.",
    llm_config=LLM_CONFIG_MOCK
)

model_selector = AutoGenToolAgent(
    name="Model_Selector_and_Tuner",
    system_message="Analyze the raw training metrics and the problem type. Select the best model and determine the final business value based on the metrics. **Your final output must be the final report content in Markdown.**",
    llm_config=LLM_CONFIG_MOCK
)

# --- Deployment & Reporting Team (Core 2 Agents) ---
reporter_git_manager = AutoGenToolAgent(
    name="Reporter_and_GitHub_Manager",
    system_message="Draft the final report and commit it. Use the `github_commit_function` tool with the Markdown content from the Model_Selector.",
    llm_config=LLM_CONFIG_MOCK
)

# --- Group the rest of the 27+ roles into a single specialized Assistant Agent for Autogen ---
specialized_automl_assistant = AssistantAgent(
    name="Specialized_AutoML_Assistant",
    system_message="You are the combined expertise of 20+ specialized agents (Auditors, Deployers, Validators, Tuners, all Trainers). You answer questions delegated by other agents using your vast knowledge base to provide detailed, technical outputs (like monitoring plans, CI/CD steps, or business quantification).",
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

# The remaining 20+ agents are represented by the detailed system message of the 
# 'Specialized_AutoML_Assistant' to simplify the AutoGen Group Chat.
