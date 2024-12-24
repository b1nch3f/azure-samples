import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

extn = "pdf"
file_name = f"CRLA-617-2010.{extn}"
file_path = os.path.join(".", "data", "documents", file_name)
print(file_path)

with open(file_path, "rb") as f:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-layout", document=f
    )
result = poller.result()

lines = []

for page in result.pages:
    for line_idx, line in enumerate(page.lines):
        # print(line.content)
        lines.append(line.content)

directory = "data/extracts"

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

extn = "txt"
# Specify the file name
file_name = f"CRLA-617-2010.{extn}"
file_path = os.path.join(directory, file_name)

# Write the lines to the file
with open(file_path, "w", encoding="utf-8") as file:
    for line in lines:
        file.write(line + "\n")

print(f"Lines saved to {file_name}")
