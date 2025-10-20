# tools/email_checker.py (AutoML Mock Logic - MODIFIED for AutoGen)
import os
import imaplib
import email
import random
from dotenv import load_dotenv

load_dotenv() 

# --- IMAP Tool (Function) ---
def email_check_function(search_terms: str) -> str:
    """
    Connects to a real IMAP inbox to search for critical, data-science related alert keywords 
    in unread email subjects. Returns the subject of the first urgent email found.
    """
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
                "Action must be taken immediately. The next step is to initiate a new, specific data investigation task."
            )
        
        mail.logout()
        return "SUCCESS: Alert found but failed to fetch subject. Proceeding with caution."

    except imaplib.IMAP4.error as e:
        return f"ERROR: Failed to connect to IMAP server. Check credentials/App Password. IMAP Error: {e}"
    except Exception as e:
        return f"UNEXPECTED ERROR: {e}"

# --- Data Processor Tool (The AutoML Mock Engine - Function) ---
def data_processor_function(task_description: str) -> str:
    """
    Performs mock data operations: Downloads a dataset, analyzes the target variable, 
    simulates data prep, and simulates training for over 20 ML/DL algorithms.
    """
    if "download and analyze dataset" in task_description.lower():
        problem_types = ["Regression", "Binary Classification", "Multi-Class Classification", "Clustering"]
        problem_type = random.choice(problem_types)
        
        return (
            f"SUCCESS: Dataset downloaded from mock client storage. "
            f"Initial Data Analysis Complete: The problem type is identified as **{problem_type}**. "
            f"Ready for Data Prep and Model Selection."
        )
        
    if "clean and feature" in task_description.lower():
        return "Data preparation simulated: Missing values handled, features engineered. Final dataset is ready for comprehensive modeling."

    if "train all models" in task_description.lower() or "simulated comprehensive training" in task_description.lower():
        return (
            "COMPREHENSIVE TRAINING SIMULATED: Initial metrics for all required algorithms have been computed in parallel. "
            "--- REGRESSION RESULTS (RMSE) ---\n"
            "LinearRegression: 0.85 | RandomForestRegressor: 0.45 | **XGBoostRegressor: 0.31** | LSTM (Forecasting): **0.30**.\n"
            "--- CLASSIFICATION RESULTS (AUC) ---\n"
            "RandomForestClassifier: 0.91 | **XGBoostClassifier: 0.95**.\n"
            "The **Model Selector** must now analyze these results based on the problem type identified earlier."
        )
        
    return f"General data processing task simulated for: {task_description}"

# --- Email Communicator Tool (Mock Send - Function) ---
def email_communicator_function(recipient: str, subject: str, body: str) -> str:
    """
    Tool to compose and 'send' (simulate) an email to the client in simple, conversational English.
    """
    final_recipient = os.getenv("CLIENT_EMAIL", recipient)
    
    log_file = "automation_logs/email_log.txt"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    with open(log_file, "a") as f:
        f.write(f"\n--- SENT EMAIL ({final_recipient}) ---\n")
        f.write(f"Subject: {subject}\n")
        f.write(f"Body:\n{body}\n")
        f.write("--------------------------------\n")
        
    return (
        f"SUCCESS: Email successfully composed and SIMULATED for client '{final_recipient}'. "
        f"Confirmation logged to {log_file}."
    )
