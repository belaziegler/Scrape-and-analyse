import re
from typing import List

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from flask import Flask, render_template, request

app = Flask(__name__)


def fetch_company_info(url: str) -> dict:
    """Retrieve team, location and financing information from a company webpage."""
    info = {"team": "Unknown", "location": "Unknown", "financing": "Unknown"}
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        return info

    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator="\n").lower()
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines:
        if "team" in line and info["team"] == "Unknown" and len(line) < 120:
            info["team"] = line
        if any(word in line for word in ["location", "headquarters", "based in"]) and info["location"] == "Unknown":
            info["location"] = line
        if any(word in line for word in ["funding", "raised", "financing"]) and info["financing"] == "Unknown":
            info["financing"] = line
        if all(value != "Unknown" for value in info.values()):
            break
    return info


def search_startups(query: str) -> List[dict]:
    ddgs = DDGS()
    results = ddgs.text(query + " startup", max_results=3)
    companies = []
    for r in results:
        info = fetch_company_info(r["href"])
        companies.append(
            {
                "name": r["title"],
                "summary": r["body"],
                "link": r["href"],
                "team": info["team"],
                "location": info["location"],
                "financing": info["financing"],
            }
        )
    return companies


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query", "")
    companies = search_startups(query)
    return render_template("results.html", results=companies, query=query)


if __name__ == "__main__":
    app.run(debug=True)
