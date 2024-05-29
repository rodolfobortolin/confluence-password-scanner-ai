import csv
import logging
import os
import re
from openai import OpenAI
import requests
from requests.auth import HTTPBasicAuth

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Constants and configuration
OPENAI_API_KEY = ""  # Create one here: https://platform.openai.com/api-keys
PROCESSED_PAGES_FILE = 'processed_pages.csv'
CLOUD_BASE_URL = "https://domain.atlassian.net"
AUTH = HTTPBasicAuth('', '')
HEADERS = {"Accept": "application/json"}

def read_processed_pages():
    """Read processed page IDs from a CSV file and return them as a set."""
    if not os.path.exists(PROCESSED_PAGES_FILE):
        return set()
    with open(PROCESSED_PAGES_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        return {rows[0] for rows in reader}

def write_processed_page(page_id, page_url, threat_count):
    """Write a processed page ID, URL, and threat count to a CSV file."""
    with open(PROCESSED_PAGES_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([page_id, page_url, threat_count])

def check_page_for_passwords(page_content):
    prompt = """I need to know if my users are storing passwords inside confluence pages, which is a bad practice and it's not allowed. I need you to verify this content and get the list of possible strings that are passwords. Be concise and just list me the words.

    Check this content: "{}" """.format(page_content)

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an assistant that will detect passwords inside texts that are stored in Confluence pages."},
                {"role": "user", "content": "I need to know if my users are storing passwords inside confluence pages, which is a bad practice and it's not allowed. I need you to verify this content and get the list of possible strings that are passwords. Be concise and just list me the words, ok?\n\nYou need to answer in this format:\n\nI Detect {number of passwords/api keys} passwords/api keys.\n\n- <list of passwords>"},
                {"role": "assistant", "content": "Ok"},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response.choices[0].message.content
        

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return ""

def list_confluence_spaces():
    """Retrieve a list of all Confluence spaces."""
    response = requests.get(f"{CLOUD_BASE_URL}/wiki/rest/api/space", auth=AUTH, headers=HEADERS)
    response.raise_for_status()
    return response.json()['results']

def get_all_pages_for_space(space_key):
    """Retrieve all pages for a given Confluence space."""
    pages = []
    start = 0
    limit = 25

    while True:
        response = requests.get(f"{CLOUD_BASE_URL}/wiki/rest/api/content", params={"spaceKey": space_key, "start": start, "limit": limit}, auth=AUTH, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        pages.extend(data['results'])
        if 'next' not in data['_links']:
            break
        start += limit

    return pages

def get_page_content(page_id):
    """Retrieve the content of a Confluence page by its ID."""
    response = requests.get(f"{CLOUD_BASE_URL}/wiki/rest/api/content/{page_id}?expand=body.storage", auth=AUTH, headers=HEADERS)
    response.raise_for_status()
    return response.json()['body']['storage']['value']

def main():
    processed_pages = read_processed_pages()
    spaces = list_confluence_spaces()
    for space in spaces:
        space_key = space['key']
        pages = get_all_pages_for_space(space_key)
        logging.info(f"Retrieved {len(pages)} pages for space {space_key}")
        for page in pages:
            page_id = page['id']
            if page_id in processed_pages:
                continue  # Skip processing if page has been processed before
            page_title = page['title']
            page_url = f"{CLOUD_BASE_URL}/wiki{page['_links']['webui']}"
            html_content = get_page_content(page_id)

            answer = check_page_for_passwords(html_content)
            if not answer:
                logging.info(f"Space {space_key} Page Title: {page_title}: No response from GPT")
                continue

            threats_detected = re.search(r"I Detect (\d+) passwords/api keys", answer)
            threat_count = threats_detected.group(1) if threats_detected else '0'
            if threat_count != '0':
                logging.warning(f"Space {space_key} Page Title: {page_title} URL: {page_url} ChatGPT: {answer} \n")
                write_processed_page(page_id, page_url, threat_count)  # Record the URL and threat count only if at least one threat is detected
            else:
                logging.info(f"Space {space_key} Page Title: {page_title}: No threats")

if __name__ == "__main__":
    main()
