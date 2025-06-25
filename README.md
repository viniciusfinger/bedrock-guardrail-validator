# Bedrock Guardrail Validator ✅🛡️

Validate the effectiveness of Amazon Bedrock guardrails automatically. This project runs tests from a ground truth set of messages, compares the expected results with those filtered by the guardrail, and generates a detailed PDF report.

## Features

- **Automated guardrail validation**: Test if the guardrail is correctly filtering sensitive messages.
- **PDF report**: Automatically generates a report with accuracy metrics and error examples.
- **Easy setup**: Just fill in a JSON file with your test cases.

## Prerequisites

- **Python 3.8+**
- **Configured AWS credentials** (for Bedrock access)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/viniciusfinger/bedrock-guardrail-validator
   cd bedrock-guardrail-validator
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Fill in the `ground_truth.json` file**

   Create a file named `ground_truth.json` in the project root with the following format:
   ```json
   [
     {
       "message": "Text to be tested",
       "should_filter": true
     },
     {
       "message": "Another safe text",
       "should_filter": false
     }
     // ... more test cases
   ]
   ```
   - `message`: The text that will be sent to the guardrail.
   - `should_filter`: `true` if the text should be blocked/intervened by the guardrail, `false` otherwise.

2. **Configure the Guardrail**

   In the `main.py` file, set the variables:
   - `GUARDRAIL_ID`: The ID of the guardrail to be tested.
   - `GUARDRAIL_VERSION`: The guardrail version (e.g., "DRAFT" or a version number).

3. **Run the validator**
   
   ```bash
   python main.py
   ```
   The script will:
   - Process all cases from `ground_truth.json`.
   - Generate an `output.json` file with the results.
   - Generate a PDF report named `guardrail_report.pdf`.

## Generated Report

The PDF report includes:
- Total processed entries
- Number of correct guardrail hits
- Accuracy (%)
- Table with examples of messages that were not filtered correctly

## Customization

- You can modify the script to adapt the evaluation logic, input or output formats as needed.
- The report can be customized by editing the `report.py` file.