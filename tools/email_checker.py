# tools/email_checker.py (REAL IMAP + AutoML MOCK LOGIC)
import os
import imaplib
import email
import random
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
from dotenv import load_dotenv

load_dotenv() 

# --- IMAP Tool ---
class EmailCheckInput(BaseModel):
    search_terms: str = Field(description="Comma-separated keywords to search in unread email subjects, e.g., 'model drift, production error, sales crash'.")

class EmailCheckerTool(BaseTool):
    name: str = "Critical Alert Inbox Checker"
    description: str = "Connects to a real IMAP inbox to search for critical, data-science related alert keywords in unread email subjects. Returns the subject of the first urgent email found."
    args_schema: Type[BaseModel] = EmailCheckInput
    
    def _run(self, search_terms: str) -> str:
        # Load credentials from GitHub Actions secrets (via os.getenv)
        IMAP_SERVER = os.getenv("IMAP_SERVER")
        IMAP_PORT = os.getenv("IMAP_PORT")
        IMAP_USERNAME = os.getenv("IMAP_USERNAME")
        IMAP_APP_PASSWORD = os.getenv("IMAP_APP_PASSWORD")

        if not all([IMAP_SERVER, IMAP_USERNAME, IMAP_APP_PASSWORD]):
            return "ERROR: IMAP credentials missing. Cannot connect to real inbox. Aborting check."

        try:
            # 1. Connect and Log in
            mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            mail.login(IMAP_USERNAME, IMAP_APP_PASSWORD)
            mail.select('inbox')
            
            # Create the IMAP search query for UNSEEN emails with any specified subject terms
            terms = [term.strip().upper() for term in search_terms.split(',')]
            search_query = '(UNSEEN ' + ' '.join([f'SUBJECT "{term}"' for term in terms]) + ')'
            
            # 2. Search for matching emails
            status, messages = mail.search(None, search_query)
            
            if status != 'OK':
                mail.logout()
                return f"ERROR: IMAP Search failed with status: {status}"

            email_ids = messages[0].split()
            
            if not email_ids:
                mail.logout()
                return "SUCCESS: No critical data science alerts found in the inbox. Proceed with scheduled tasks."
            
            # 3. Retrieve and Parse the First Alert
            status, msg_data = mail.fetch(email_ids[0], '(RFC822)')
            
            if status == 'OK':
                msg = email.message_from_bytes(msg_data[0][1])
                subject = msg['Subject']
                
                # Mark the email as read
                mail.store(email_ids[0], '+FLAGS', '\\Seen')
                
                mail.logout()
                return (
                    f"CRITICAL ALERT FOUND: Subject: '{subject}'. "
                    "This email contained one of the critical keywords. "
                    "Action must be taken immediately. The next step is to initiate a new, specific data investigation task."
                )
            
            mail.logout()
            return "SUCCESS: Alert found but failed to fetch subject. Proceeding with caution."

        except imaplib.IMAP4.error as e:
            return f"ERROR: Failed to connect to IMAP server. Check credentials/App Password. IMAP Error: {e}"
        except Exception as e:
            return f"UNEXPECTED ERROR: {e}"

# --- Data Processor Tool (The AutoML Mock Engine) ---
class DataProcessorTool(BaseTool):
    name: str = "Data Processor Tool"
    description: "Performs mock data operations: Downloads a dataset, analyzes the target variable (Regression, Classification, Clustering), simulates data prep, and simulates training for over 20 ML/DL algorithms, returning metrics."
    
    def _run(self, task_description: str) -> str:
        
        # 1. MOCK DATA DOWNLOAD AND ANALYSIS
        if "download and analyze dataset" in task_description.lower():
            # Mock analysis logic: We'll randomly select a problem type to simulate variety.
            problem_types = ["Regression", "Binary Classification", "Multi-Class Classification", "Clustering"]
            problem_type = random.choice(problem_types)
            
            mock_dataset_schema = {
                "target_name": "Sales_Volatility" if "Regression" in problem_type else "Customer_Churn" if "Classification" in problem_type else "No Target",
                "problem_type": problem_type,
                "row_count": "500,000",
                "features": ["Date", "Price_Lagged", "Store_ID", "Promo_Type", "Inventory_Level"]
            }
            
            return (
                f"SUCCESS: Dataset downloaded from mock client storage. "
                f"Initial Data Analysis Complete: The problem type is identified as **{problem_type}**. "
                f"Target Variable: {mock_dataset_schema['target_name']}. "
                f"Initial Schema: {mock_dataset_schema}. Ready for Data Prep and Model Selection."
            )
            
        # 2. MOCK DATA PREPARATION
        if "clean" in task_description.lower() or "feature" in task_description.lower():
            return "Data preparation simulated: Missing values handled, features engineered (lags, rolling means, volatility index, and one-hot encoding). Final dataset is ready for comprehensive modeling."

        # 3. MOCK COMPREHENSIVE TRAINING
        if "train all models" in task_description.lower() or "simulated comprehensive training" in task_description.lower():
            # A huge block of mock results to simulate all models running in parallel
            return (
                "COMPREHENSIVE TRAINING SIMULATED: Initial metrics for all required algorithms have been computed in parallel. "
                "--- REGRESSION RESULTS (RMSE) ---\n"
                "LinearRegression: 0.85 | PolynomialFeatures+LR: 0.78 | Lasso: 0.82 | Ridge: 0.75 | ElasticNet: 0.79 | DecisionTreeRegressor: 0.55 | "
                "RandomForestRegressor: 0.45 | ExtraTreeRegressor: 0.50 | GradientBoostingRegressor: 0.35 | XGBoostRegressor: **0.31** | KNNRegressor: 0.60 | SVR: 0.70.\n"
                "--- CLASSIFICATION RESULTS (AUC) ---\n"
                "LogisticRegression: 0.75 | DecisionTreeClassifier: 0.80 | RandomForestClassifier: 0.91 | ExtraTreeClassifier: 0.85 | "
                "GradientBoostingClassifier: 0.93 | XGBoostClassifier: **0.95** | KNNClassifier: 0.70 | SVC: 0.88.\n"
                "--- CLUSTERING RESULTS (Sillhouette Score) ---\n"
                "KMeans: 0.45 | DBSCAN: 0.38 | AgglomerativeClustering: 0.42.\n"
                "--- DEEP LEARNING RESULTS (RMSE/AUC) ---\n"
                "ANN (Regression): 0.40 | CNN (Classification): 0.90 | RNN (Forecasting): 0.38 | LSTM (Forecasting): **0.30** | GRU (Forecasting): 0.33 | AutoEncoder (Anomaly): 0.05 (Reconstruction Error). "
                "The **Model Selector** must now analyze these results based on the problem type identified earlier."
            )
            
        return f"General data processing task simulated for: {task_description}"

# --- Email Communicator Tool (Mock Send) ---
class EmailCommunicatorTool(BaseTool):
    name: str = "Email Communicator"
    description: str = "Tool to compose and 'send' (simulate) an email to the client in simple, conversational English."

    def _run(self, recipient: str, subject: str, body: str) -> str:
        # Gets CLIENT_EMAIL from environment
        final_recipient = os.getenv("CLIENT_EMAIL", recipient)
        
        log_file = "automation_logs/email_log.txt"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        with open(log_file, "a") as f:
            f.write(f"\n--- SENT EMAIL ({final_recipient}) ---\n")
            f.write(f"Subject: {subject}\n")
            f.write(f"Body:\n{body}\n")
            f.write("--------------------------------\n")
            
        return (
            f"Email successfully composed and SIMULATED for client '{final_recipient}'. "
            f"Confirmation logged to {log_file}."
        )
