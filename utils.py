import requests
from bs4 import BeautifulSoup
from datetime import datetime


def extract_data(url: str) -> dict:
    results = {}
    error = ""
    try:
        # Make a request
        response = requests.get(url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        results["author"] = soup.find("meta", {"name": "parsely-author"})["content"]

        results["title"] = soup.find("meta", {"name": "parsely-title"})["content"]

        results["pub_date"] = soup.find("meta", {"name": "parsely-pub-date"})["content"]

        results["link"] = soup.find("meta", {"name": "parsely-link"})["content"]

    except Exception as e:
        error = str(e)

    return results, error


def current_timestamp():
    timestamp = datetime.now()
    return timestamp
