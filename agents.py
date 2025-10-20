# agents.py (27+ Specialized Agents for AutoML)
import os
from crewai import Agent
from langchain_community.llms import Ollama
from crewai_tools import FileReadTool
from tools.github_file_creator import GitHubFileCreatorTool
from tools.email_checker import EmailCheckerTool, DataProcessorTool, EmailCommunicatorTool
from dotenv import load_dotenv

load_dotenv()

# Initialize Local LLM (Ollama)
ollama_mistral = Ollama(model="mistral", base_url=os.getenv("OLLAMA_BASE_URL"))

# Initialize Tools
read_knowledge_tool = FileReadTool()
github_tool = GitHubFileCreatorTool()
email_tool = EmailCommunicatorTool()
data_tool = DataProcessorTool()
email_check_tool = EmailCheckerTool() 

# --- AGENT DEFINITION (27+ Agents) ---

# 1. Project Management Team (5 Agents)
project_manager = Agent(role='Executive Project Lead', goal='Define project scope, ensure all dependencies are met, and set clear business impact targets.', backstory='The primary liaison, focused on client goals and high-level strategy.', llm=ollama_mistral, verbose=True, allow_delegation=True)
inbox_monitor = Agent(role='Critical System Alert Monitor', goal='Check the monitoring inbox for high-priority data science alerts (e.g., model drift, production error).', backstory='The first line of defense, proactively detecting critical failures.', tools=[email_check_tool], llm=ollama_mistral, verbose=True)
client_liaison = Agent(role='Client Communication Strategist', goal='Translate technical outcomes into simple, conversational English for client emails.', backstory='Expert in client relations and simple, effective business language.', tools=[email_tool], llm=ollama_mistral, verbose=True)
budget_tracker = Agent(role='Budget and Time Analyst', goal='Monitor and report on project budget and time constraints.', backstory='A meticulous accountant for agent resources and task time.', llm=ollama_mistral, verbose=True)
stakeholder_reporter = Agent(role='Internal Stakeholder Reporter', goal='Generate high-level status reports for internal leadership.', backstory='Clear communicator, summarizing complex progress concisely.', llm=ollama_mistral, verbose=True)

# 2. Data Acquisition Team (4 Agents)
data_cleaner = Agent(role='Data Quality Engineer', goal='Cleanse raw data and ensure data integrity.', backstory='Obsessed with data purity and feature type consistency.', tools=[data_tool], llm=ollama_mistral, verbose=True)
feature_engineer = Agent(role='Feature Generation Specialist', goal='Create necessary features (lags, rolling means, volatility, encoding) for all ML models.', backstory='Creative mathematician who builds predictive power from raw features.', tools=[data_tool], llm=ollama_mistral, verbose=True)
data_auditor = Agent(role='Data Security and Compliance Auditor', goal='Ensure all data handling complies with security protocols and data leakage standards.', backstory='A compliance expert in data privacy and security best practices.', llm=ollama_mistral, verbose=True)
data_ingestor = Agent(role='Source System Integrator & Data Analyst', goal='Download, analyze the target variable, and understand the problem type (Regression, Classification, Clustering) of the raw client dataset.', backstory='Expert in connecting disparate systems and initial dataset profiling.', tools=[data_tool], llm=ollama_mistral, verbose=True)


# 3. Model Training Team (14 Agents)
model_selector = Agent(
    role='AutoML Algorithm Selection Specialist', 
    goal='Determine the optimal algorithms based on the problem type and select the single best-performing model from the comprehensive training simulation.', 
    backstory='Deep knowledge of statistical, ensemble, deep learning, and unsupervised algorithms.', 
    llm=ollama_mistral, verbose=True
)
regressor_ensemble_trainer = Agent(
    role='Advanced Regressor Specialist', 
    goal='Simulate training and evaluation for Linear, Lasso, Ridge, ElasticNet, DecisionTree, RandomForest, ExtraTree, GradientBoosting, and XGBoost Regressors.', 
    backstory='Expert in minimizing RMSE/MAE across all predictive regression techniques.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
classifier_ensemble_trainer = Agent(
    role='Advanced Classifier Specialist', 
    goal='Simulate training and evaluation for Logistic, DecisionTree, RandomForest, ExtraTree, GradientBoosting, and XGBoost Classifiers.', 
    backstory='Expert in maximizing AUC/F1-score across all predictive classification techniques.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
svm_knn_trainer = Agent(
    role='SVR/SVC and KNN Specialist', 
    goal='Simulate training for Support Vector Regressor/Classifier (SVR/SVC) and K-Nearest Neighbors (KNN).', 
    backstory='Specializes in distance-based and kernel-based non-linear models.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
clustering_specialist = Agent(
    role='Unsupervised Learning Specialist', 
    goal='Simulate training and evaluate clustering models: K-Means, DBSCAN, and Agglomerative Clustering.', 
    backstory='Expert in discovering hidden structures and patterns in unlabeled data.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
ann_autoencoder_trainer = Agent(
    role='ANN/AutoEncoder Specialist', 
    goal='Simulate training and evaluation for standard Artificial Neural Networks (ANN) for prediction and AutoEncoders for anomaly detection.', 
    backstory='Expert in basic deep learning architectures and feature learning.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
cnn_trainer = Agent(
    role='CNN Specialist', 
    goal='Simulate training and evaluation for Convolutional Neural Networks (CNN) on tabular/sequence data transformations.', 
    backstory='Expert in pattern recognition and feature extraction.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
rnn_gru_trainer = Agent(
    role='RNN/GRU Specialist', 
    goal='Simulate training and evaluation for Recurrent Neural Networks (RNN) and Gated Recurrent Units (GRU) for sequence prediction.', 
    backstory='Expert in short-term sequence dependency modeling.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
lstm_trainer = Agent(
    role='LSTM Deep Learning Specialist', 
    goal='Simulate training and evaluation for Long Short-Term Memory (LSTM) networks for advanced time-series forecasting.', 
    backstory='Expert in long-term sequence dependency modeling.', 
    tools=[data_tool], llm=ollama_mistral, verbose=True
)
hyperparameter_optimizer = Agent(role='Bayesian Hyperparameter Tuner', goal='Systematically tune hyperparameters for the top two performing models from the relevant problem type.', backstory='Expert in automated hyperparameter search and optimization.', llm=ollama_mistral, verbose=True)
model_validator = Agent(role='Model Validation and Testing Analyst', goal='Perform robust cross-validation and select the single best-performing model based on the business metric.', backstory='A meticulous analyst ensuring models generalize well.', llm=ollama_mistral, verbose=True)
metric_interpreter = Agent(role='Evaluation Metric Translator', goal='Translate technical metrics (RMSE/MAE/AUC/Sillhouette) into non-technical prediction terms for the business.', backstory='Focuses on the practical meaning of statistical results.', llm=ollama_mistral, verbose=True)
knowledge_ingestor = Agent(role='Business Knowledge Ingestor', goal='Use the knowledge base to inform modeling constraints and objectives.', backstory='Connects model performance directly to business goals.', tools=[read_knowledge_tool], llm=ollama_mistral, verbose=True)


# 4. Deployment & Ops Team (4 Agents)
infra_proviser = Agent(role='Infrastructure Provisioning Expert', goal='Prepare the cloud environment (mock) for model deployment.', backstory='Specialist in infrastructure as code (Terraform/CloudFormation mock).', llm=ollama_mistral, verbose=True)
monitor_agent = Agent(role='Model Monitoring Specialist', goal='Design and set up model drift and data integrity monitoring.', backstory='Focuses on post-deployment model performance and decay.', llm=ollama_mistral, verbose=True)
ci_cd_specialist = Agent(role='CI/CD Pipeline Manager', goal='Design the automated workflow for pushing the final model to production.', backstory='Expert in seamless and automated deployment pipelines.', llm=ollama_mistral, verbose=True)
deployment_auditor = Agent(role='Security and Access Auditor', goal='Verify security access and credentials for the deployment environment.', backstory='Ensures deployment credentials are secure and compliant.', llm=ollama_mistral, verbose=True)


# 5. Business & Reporting Team (1 Agent)
impact_translator = Agent(role='Business Impact Translator', goal='Quantify the project\'s final value (e.g., cost savings) for the client.', backstory='The ultimate value creator, translating predictions into dollar amounts.', llm=ollama_mistral, verbose=True, tools=[read_knowledge_tool])
