# crew.py (FINAL VERSION - 27+ AGENTS)
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from tasks import * from agents import * from langchain_community.llms import Ollama

# 1. Load environment variables
load_dotenv()

# Re-initialize the Ollama LLM
ollama_mistral = Ollama(model="mistral", base_url=os.getenv("OLLAMA_BASE_URL"))

# --- 2. Define the Crew (27+ Agents) ---
data_science_crew = Crew(
    agents=[
        # Project Management
        project_manager, client_liaison, inbox_monitor, budget_tracker, stakeholder_reporter,
        # Data Acquisition
        data_ingestor, data_cleaner, feature_engineer, data_auditor,
        # Model Training (The new specialists)
        model_selector, regressor_ensemble_trainer, classifier_ensemble_trainer, svm_knn_trainer, 
        clustering_specialist, ann_autoencoder_trainer, cnn_trainer, rnn_gru_trainer, 
        lstm_trainer, hyperparameter_optimizer, model_validator, metric_interpreter, knowledge_ingestor,
        # Deployment & Ops
        infra_proviser, monitor_agent, ci_cd_specialist, deployment_auditor,
        # Business & Reporting
        impact_translator
    ],
    tasks=[
        # The full 20-step workflow
        t_0_check_alerts, t_1_ingest_domain, t_2_scope_define, 
        t_3_ingest_data_and_analyze, t_4_clean_and_feature, t_6_data_audit,
        t_8_comprehensive_train, t_10_model_selection, t_11_tune_models, t_12_final_validate, t_13_metric_translate,
        t_14_monitor_setup, t_15_cicd_plan, t_16_deployment_audit,
        t_17_quantify_impact, t_18_final_report_draft, t_19_commit_report, t_20_send_email
    ],
    process=Process.sequential, 
    manager_llm=ollama_mistral, 
    verbose=2,
    full_output=True
)

# --- 3. Run the Crew ---
if __name__ == "__main__":
    print(f"--- 🚀 Starting Autonomous Data Scientist Crew (AutoML) with LLM: {os.getenv('OLLAMA_BASE_URL')} ---")
    
    result = data_science_crew.kickoff(
        inputs={'project_topic': 'Dynamic Client Problem Resolution'}
    )
    
    print("\n\n################################################")
    print("### CREW EXECUTION COMPLETE (AutoML Pipeline) ###")
    print("################################################")
    print(result)
