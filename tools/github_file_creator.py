# tools/github_file_creator.py
import os
from typing import Type
from pydantic import BaseModel, Field
from crewai_tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

class GitHubFileCreatorInput(BaseModel):
    file_path: str = Field(description="The full path and file name for the new file (e.g., 'reports/final_summary.md').")
    content: str = Field(description="The content to be written to the file (the final report in Markdown format).")
    commit_message: str = Field(description="The commit message to use for the GitHub action.")

class GitHubFileCreatorTool(BaseTool):
    name: str = "GitHub File Creator"
    description: str = "A tool to simulate creating or updating a file in a GitHub repository using local file system changes. It requires the file path, content, and a commit message."
    args_schema: Type[BaseModel] = GitHubFileCreatorInput
    
    def _run(self, file_path: str, content: str, commit_message: str) -> str:
        # 1. Simulate local file creation 
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(content)
        except Exception as e:
            return f"ERROR: Failed to simulate local file creation: {e}"

        # 2. Simulate GitHub status check 
        repo_owner = os.getenv("GITHUB_REPO_OWNER", "MOCK_OWNER")
        repo_name = os.getenv("GITHUB_REPO_NAME", "MOCK_REPO")
        
        return (
            f"SUCCESS: File '{file_path}' created/updated locally. "
            f"GitHub action simulated: Content committed to '{repo_owner}/{repo_name}' "
            f"with message: '{commit_message}'. Ready for deployment."
        )
