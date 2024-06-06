## Overview

This script is a Proof of Concept (POC) designed to fetch the service catalog from a Jira Service Management portal and use OpenAI API to classify information for Service Desk Portals. The script retrieves request types and their descriptions, stores them in a CSV file, and then uses OpenAI to process and classify the data.

## Prerequisites

- Python 3.6+
- OpenAI API key
- Requests library
- OpenAI library

## Setup

1. **Clone the repository:**
    ```bash
    git clone git@github.com:rodolfobortolin/request-ai-classification.git
    cd request-ai-classification
    ```

2. **Install required Python packages:**
    ```bash
    pip install requests openai
    ```

3. **Configuration:**
   - Update the `cloud` dictionary with your Jira Service Management username, API token, and base URL.
   - Update the `OPENAI_API_KEY` with your OpenAI API key.

4. **Logging Configuration:**
   - The script uses the `logging` module to log information. Modify the logging configuration if needed.

## Usage

1. **Run the Script:**
    ```bash
    python main.py
    ```

2. **Output:**
   - The script will create a CSV file named `Service Catalog.csv` containing the service catalog data.
   - The script will log the classification response from OpenAI.

## Script Details

### Functions

- **fetch_service_catalog():**
  - Fetches the service catalog from the Jira Service Management portal.
  - Saves the service catalog data to a CSV file.

- **get_csv_content_as_text(csv_file_path):**
  - Reads the content of the CSV file as text.

- **process_catalog(writer):**
  - Uses OpenAI API to classify the service catalog data.
  - Returns the classification response.

### Main Process

1. Fetches the service catalog and saves it to a CSV file.
2. Reads the CSV content.
3. Processes the CSV content using OpenAI API.
4. Logs the classification response.
