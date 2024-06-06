
# README.md

## Overview

This script is designed to scan Confluence pages for any stored passwords, which is a bad practice and not allowed. It leverages the OpenAI API to detect potential passwords within the page content and logs the results. Processed pages are tracked to avoid redundant scans.

## Prerequisites

- Python 3.6+
- OpenAI API key
- Requests library
- OpenAI library

## Setup

1. **Clone the repository:**
    ```bash
    git clone git@github.com:rodolfobortolin/confluence-password-scanner-ai.git
    cd confluence-password-scanner-ai
    ```

2. **Install required Python packages:**
    ```bash
    pip install requests openai
    ```

3. **Configuration:**
   - Update the `OPENAI_API_KEY` with your OpenAI API key. You can create one [here](https://platform.openai.com/api-keys).
   - Set the `CLOUD_BASE_URL` to your Confluence domain.
   - Set up the `AUTH` with your Confluence username and API token.

4. **Logging Configuration:**
   - The script uses the `logging` module to log information. Modify the logging configuration if needed.

## Usage

1. **Run the Script:**
    ```bash
    python main.py
    ```

2. **Processed Pages:**
   - The script maintains a record of processed pages in a CSV file (`processed_pages.csv`) to avoid redundant processing.

## Script Details

### Functions

- **read_processed_pages():**
  Reads processed page IDs from a CSV file and returns them as a set.

- **write_processed_page(page_id, page_url, threat_count):**
  Writes a processed page ID, URL, and threat count to a CSV file.

- **check_page_for_passwords(page_content):**
  Uses OpenAI API to check the content for potential passwords and returns the response.

- **list_confluence_spaces():**
  Retrieves a list of all Confluence spaces.

- **get_all_pages_for_space(space_key):**
  Retrieves all pages for a given Confluence space.

- **get_page_content(page_id):**
  Retrieves the content of a Confluence page by its ID.

### Main Process

1. Reads the processed pages.
2. Retrieves a list of all Confluence spaces.
3. For each space, retrieves all pages and processes them.
4. Checks each page content for potential passwords using the OpenAI API.
5. Logs and records the pages with detected passwords.
