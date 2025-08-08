import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Pfad zum src-Verzeichnis hinzufügen, damit "app" importiert werden kann
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from app import fetch_company_info, search_startups


def test_fetch_company_info_extracts_fields():
    html = "<html><body>our team is small\nwe are based in berlin\nraised $2M in funding</body></html>"
    mock_resp = Mock(status_code=200, text=html)
    mock_resp.raise_for_status = Mock()

    with patch("requests.get", return_value=mock_resp):
        info = fetch_company_info("http://example.com")

    assert info["team"] == "our team is small"
    assert info["location"] == "we are based in berlin"
    assert info["financing"] == "raised $2m in funding"


def test_search_startups_includes_scraped_info():
    fake_results = [
        {
            "title": "Test Startup",
            "body": "Testing things",
            "href": "http://example.com",
        }
    ]

    with patch("app.DDGS") as mock_ddgs, patch("app.fetch_company_info") as mock_info:
        mock_ddgs.return_value.text.return_value = fake_results
        mock_info.return_value = {
            "team": "team line",
            "location": "location line",
            "financing": "financing line",
        }
        companies = search_startups("ai")

    assert companies[0]["name"] == "Test Startup"
    assert companies[0]["team"] == "team line"
    assert companies[0]["location"] == "location line"
    assert companies[0]["financing"] == "financing line"
