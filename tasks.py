# tasks.py (Dynamic 20-Step Workflow)
import os
from crewai import Task
from agents import * from pydantic import BaseModel, Field

# Schema for structured output of the final model selection
class FinalModelEvaluation(BaseModel):
    model_name: str = Field(description="The name of the single best-performing model (e.g., 'XGBoostRegressor' or 'LSTM').")
    key_metric_score: float = Field(description="The final, optimized metric score (e.g., RMSE value or AUC score).")
    simple_performance_summary: str = Field(description="A single sentence explaining the model's accuracy in simple English.")

# --- 1. PRE-FLIGHT TASK (The Continuous Check) ---
t_0_check_alerts = Task(
    description="**Use the 'Critical Alert Inbox Checker' tool** to scan the monitoring email for critical, data-science related alerts. Search terms: 'model drift, production error, sales crash, forecast failure'. This must be the very first action.",
    expected_output="A clear statement indicating 'CRITICAL ALERT FOUND' with the email subject, or 'No critical data science alerts found'.",
    agent=inbox_monitor, 
    tools=[email_check_tool] 
)

# --- 2. PROJECT SCOPING PHASE ---
t_1_ingest_domain = Task(
    description="Read the 'knowledge/client_domain.txt' and 'knowledge/business_metrics.md' files to internalize client industry context and key business outcomes.",
    expected_output="A concise summary of the client's business domain and the 3 most critical business metrics.",
    agent=knowledge_ingestor,
    context=[t_0_check_alerts]
)

t_2_scope_define = Task(
    description="Define the exact project success metrics and **take the result of the email check (T0) into account** to decide if the forecast task should be aborted for an immediate crisis response. If CRITICAL ALERT was found, goal shifts to 'Investigate and Mitigate Production Error'.",
    expected_output="A Pydantic object detailing the project's goal, the two key success metrics, and the final business impact outcome (e.g., 'reduce overstock cost by $X per month' or 'Immediate model fix').",
    agent=project_manager,
    context=[t_1_ingest_domain, t_0_check_alerts]
)

# --- 3. DATA ACQUISITION & FEATURE ENGINEERING PHASE (DYNAMIC ANALYSIS) ---
t_3_ingest_data_and_analyze = Task(
    description="**Use the Data Processor Tool** to simulate downloading the client dataset and analyze the target variable. The output must clearly state the **PROBLEM TYPE** (Regression, Classification, or Clustering).",
    expected_output="A report confirming dataset analysis is complete, explicitly stating the 'PROBLEM TYPE' and the initial schema.",
    agent=data_ingestor,
    tools=[data_tool],
    context=[t_2_scope_define]
)

t_4_clean_and_feature = Task(
    description="Use the Data Processor Tool (via Data Cleaner and Feature Engineer) to clean the raw data, handle missing values, and create all necessary features (e.g., polynomial features, lagged values, and categorical encodings) required for the full suite of ML/DL algorithms.",
    expected_output="A report confirming data quality issues fixed and all advanced features created, ready for comprehensive modeling.",
    agent=feature_engineer, 
    context=[t_3_ingest_data_and_analyze],
    tools=[data_tool]
)

t_6_data_audit = Task(
    description="Audit the final cleaned and featured dataset for compliance (mock PII) and report on the data's readiness.",
    expected_output="A confirmation of a clean/safe dataset ready for the modeling team.",
    agent=data_auditor,
    context=[t_4_clean_and_feature]
)

# --- 4. MODEL TRAINING & SELECTION PHASE (COMPREHENSIVE) ---
t_8_comprehensive_train = Task(
    description="**Use the Data Processor Tool (via Regressor/Classifier/DL specialists)** to simulate the simultaneous training and evaluation of ALL required algorithms: Regression (12), Classification (8), Clustering (3), and Deep Learning (6). The output must be the large table of mock results provided by the Data Processor Tool.",
    expected_output="The comprehensive, structured table of initial performance metrics (RMSE, AUC, Silhouette, Reconstruction Error) for all 29 algorithms.",
    agent=regressor_ensemble_trainer, 
    context=[t_6_data_audit],
    tools=[data_tool]
)

t_10_model_selection = Task(
    description="**Analyze the comprehensive results (T8) and the PROBLEM TYPE (T3)**. Identify the single, best-performing model from the RELEVANT category. Briefly justify the selection.",
    expected_output="The name and initial metric of the single, best model for the identified problem type (e.g., 'XGBoostRegressor with RMSE=0.31').",
    agent=model_selector,
    context=[t_3_ingest_data_and_analyze, t_8_comprehensive_train]
)

t_11_tune_models = Task(
    description="Focus hyperparameter tuning on the single best model identified in T10 to maximize its performance based on the primary business metric defined in T2.",
    expected_output="The final, optimized hyperparameters for the best model and the resulting final metric improvement (e.g., 'Final RMSE improved to 0.28').",
    agent=hyperparameter_optimizer,
    context=[t_10_model_selection],
    tools=[data_tool] 
)

t_12_final_validate = Task(
    description="Perform the final cross-validation on the tuned model and output the final result in the structured Pydantic format.",
    agent=model_validator,
    context=[t_11_tune_models],
    output_json=FinalModelEvaluation 
)

t_13_metric_translate = Task(
    description="Take the best model's final metrics (from T12) and translate them into a simple, single paragraph explaining the performance in non-technical, simple conversational English for the client.",
    expected_output="One simple English paragraph about model performance, ready for the client.",
    agent=metric_interpreter,
    context=[t_12_final_validate]
)

# --- 5, 6, 7 (DEPLOYMENT, BUSINESS, COMMUNICATION) ---

t_14_monitor_setup = Task(
    description="Design the monitoring dashboard, focusing on model drift metrics and data integrity checks for the production environment.",
    expected_output="A 3-point plan for production model monitoring, including which metrics to track.",
    agent=monitor_agent,
    context=[t_13_metric_translate]
)

t_15_cicd_plan = Task(
    description="Develop the final CI/CD pipeline plan to automatically deploy the model to the mock infrastructure upon final approval.",
    expected_output="A brief, ordered list (YAML-like) of steps for the automated deployment pipeline.",
    agent=ci_cd_specialist,
    context=[t_14_monitor_setup]
)

t_16_deployment_audit = Task(
    description="Review the CI/CD plan and monitor setup. Verify mock security and access for the deployment environment.",
    expected_output="A confirmation that the deployment plan is secure and ready for implementation.",
    agent=deployment_auditor,
    context=[t_15_cicd_plan]
)

t_17_quantify_impact = Task(
    description="Using the project scope (T2), the final metric translation (T13), and the ingested business knowledge, quantify the final, *real* business impact in dollar amounts or percentage savings.",
    expected_output="A clear, quantified statement of the project's value (e.g., 'The model is projected to save $X,000 annually by reducing stock-outs.').",
    agent=impact_translator,
    context=[t_2_scope_define, t_13_metric_translate]
)

t_18_final_report_draft = Task(
    description="Draft the final, comprehensive client report in Markdown. The report must include the Business Impact (T17), the Model Performance (T13), and the Deployment Plan (T15).",
    expected_output="The complete, polished final report in clean Markdown format.",
    agent=stakeholder_reporter,
    context=[t_17_quantify_impact, t_15_cicd_plan]
)

t_19_commit_report = Task(
    description="Take the final report from the context (T18). **Use the 'GitHub File Creator' tool** to commit it to the repo: 'client_reports/final_volatility_forecast_report.md' with commit message: 'docs: Automated Final Client Report.'",
    expected_output="A confirmation message of the successful GitHub commit, including the full file path.",
    agent=client_liaison, 
    context=[t_18_final_report_draft],
    tools=[github_tool]
)

t_20_send_email = Task(
    description="Draft a simple, conversational email to the client summarizing the final Business Impact (T17) and mentioning the report is now on GitHub. **Use the 'Email Communicator' tool** to 'send' the final communication to the recipient defined by the CLIENT_EMAIL environment variable.",
    expected_output="A confirmation message that the email was successfully composed and logged.",
    agent=client_liaison,
    context=[t_17_quantify_impact, t_19_commit_report],
    tools=[email_tool]
)
