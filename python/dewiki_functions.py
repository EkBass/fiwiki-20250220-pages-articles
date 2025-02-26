from threading import Thread, Lock
import json
import re
from html2text import html2text as htt
import wikitextparser as wtp
import os

lock = Lock()  # Thread lock to ensure safe writes to the JSON file

DATA_FILE = "data.json"


def dewiki(text):
    """Convert wiki markup to clean plain text."""
    text = wtp.parse(text).plain_text()  # Convert wiki to plaintext
    text = htt(text)  # Remove any HTML
    text = text.replace('\\n', ' ')  # Replace newlines
    text = re.sub(r'\s+', ' ', text)  # Replace excess whitespace
    return text


def analyze_chunk(text):
    """Extract title, ID, and clean content from a Wikipedia article chunk."""
    try:
        if '<redirect title="' in text:  # Skip redirects
            return None
        if '(disambiguation)' in text:  # Skip disambiguation pages
            return None
        else:
            title = text.split('<title>')[1].split('</title>')[0]
            title = htt(title)
            if ':' in title:  # Skip non-main namespace pages
                return None
        serial = text.split('<id>')[1].split('</id>')[0]
        content = text.split('</text')[0].split('<text')[1].split('>', maxsplit=1)[1]
        content = dewiki(content)
        return {'title': title.strip(), 'text': content.strip(), 'id': serial.strip()}
    except Exception as e:
        print(f"Error processing article: {e}")
        return None


def save_article(article):
    """Append the article to a single JSON file in a thread-safe way."""
    doc = analyze_chunk(article)
    if doc:
        print(f"SAVING: {doc['title']}")
        with lock:  # Ensure only one thread writes at a time
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r+", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                        if isinstance(data, list):
                            data.append(doc)
                        else:
                            data = [doc]  # If file is corrupted or not a list, reset it
                    except json.JSONDecodeError:
                        data = [doc]  # Start a new list if the file is empty or broken
                    f.seek(0)  # Move cursor to the beginning of the file
                    json.dump(data, f, sort_keys=True, indent=1, ensure_ascii=False)
                    f.truncate()  # Remove old data beyond the new end
            else:
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump([doc], f, sort_keys=True, indent=1, ensure_ascii=False)


def process_file_text(filename):
    """Read and process the Wikipedia dump file."""
    article = ''
    with open(filename, 'r', encoding='utf-8') as infile:
        for line in infile:
            if '<page>' in line:
                article = ''
            elif '</page>' in line:  # End of article
                Thread(target=save_article, args=(article,)).start()
            else:
                article += line
