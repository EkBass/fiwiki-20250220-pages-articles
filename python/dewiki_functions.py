import json
import re
import os
import time
from html2text import html2text as htt
import wikitextparser as wtp

from threading import Lock

lock = Lock()  # Thread lock to ensure safe writes

# Base filename format
DATA_FILE_TEMPLATE = "data{}.json"

# Global counters
article_count = 0  # Total articles processed
batch = []  # Stores articles before writing
file_index = 1  # Used for switching data.json files

def dewiki(text):
    """Convert wiki markup to clean plain text."""
    text = wtp.parse(text).plain_text()  # Convert wiki to plaintext
    text = htt(text)  # Remove any HTML
    text = text.replace('\\n', ' ')  # Replace newlines
    text = re.sub(r'\s+', ' ', text)  # Replace excess whitespace
    return text.strip()


def analyze_chunk(text):
    """Extract title, ID, and clean content from a Wikipedia article chunk."""
    try:
        if '<redirect title="' in text:  # Skip redirects
            return None
        if '(disambiguation)' in text:  # Skip disambiguation pages
            return None
        if '<title>' in text:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:  # Skip non-main namespace pages
                return None
        if '<id>' in text:
            serial = text.split('<id>')[1].split('</id>')[0]
        else:
            return None
        if '<text' in text and '</text' in text:
            content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
            content = dewiki(content)
        else:
            return None

        return {'title': title.strip(), 'text': content.strip(), 'id': serial.strip()}
    except Exception as e:
        print(f"Error processing article: {e}")
        return None


def save_articles():
    """Saves batch of articles to JSON file safely."""
    global batch, article_count, file_index

    if batch:
        filename = DATA_FILE_TEMPLATE.format(file_index)

        with lock:
            if os.path.exists(filename):
                with open(filename, "r+", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, list):
                            data.extend(batch)
                        else:
                            data = batch  # If file is corrupted or not a list, reset it
                    except json.JSONDecodeError:
                        data = batch  # Start a new list if the file is empty or broken
                    f.seek(0)  # Move cursor to the beginning of the file
                    json.dump(data, f, sort_keys=True, indent=1, ensure_ascii=False)
                    f.truncate()
            else:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(batch, f, sort_keys=True, indent=1, ensure_ascii=False)

        batch = []  # Clear batch after writing

        # Print progress every 1000 articles
        if article_count % 1000 == 0:
            timestamp = time.strftime("%H:%M:%S")
            print(f"{article_count} articles processed at {timestamp}")

        # Rotate file every 10,000 articles
        if article_count % 10000 == 0:
            file_index += 1


def process_file_text(filename):
    """Reads and processes the Wikipedia dump file in batches."""
    global article_count, batch

    article = ''
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<page>' in line:
                article = ''
            elif '</page>' in line:  # End of article
                doc = analyze_chunk(article)
                if doc:
                    batch.append(doc)
                    article_count += 1

                # Save batch every 500 articles
                if len(batch) >= 500:
                    save_articles()
            else:
                article += line

    # Save any remaining articles at the end
    if batch:
        save_articles()
