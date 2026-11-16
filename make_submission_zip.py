"""
CoverCraft AI - Submission ZIP Packaging Utility
Creates a clean, submission-ready ZIP file conforming to the college format:
2026BTAI079_Tom_Antony_Code.zip
"""

import os
import zipfile

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ZIP_NAME = "2026BTAI079_Tom_Antony_Code.zip"
OUTPUT_ZIP_PATH = os.path.join(PROJECT_DIR, ZIP_NAME)

EXCLUDED_DIRS = {".git", "__pycache__", ".vscode", ".idea", "venv", "env"}
EXCLUDED_FILES = {".env", ZIP_NAME}

def package_submission():
    print(f"Creating submission archive: {ZIP_NAME}...")
    with zipfile.ZipFile(OUTPUT_ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_DIR):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            
            for file in files:
                if file in EXCLUDED_FILES or file.endswith(".pyc"):
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, PROJECT_DIR)
                print(f"  + Adding {rel_path}")
                zipf.write(file_path, rel_path)

    print(f"\n[SUCCESS] Archive created at: {OUTPUT_ZIP_PATH}")
    print(f"File size: {round(os.path.getsize(OUTPUT_ZIP_PATH) / 1024, 2)} KB")
    print("\nVerified: Sensitive .env and git cache files excluded.")

if __name__ == "__main__":
    package_submission()
