import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

URL = "https://queue-times.com/parks/1/queue_times.json"
CALENDAR_URL = "https://queue-times.com/parks/1/calendar"


def fetch_live_data():
    try:
        return requests.get(URL, timeout=10).json()
    except:
        return None


def get_ride_info(data, ride_name):
    if data is None:
        return False, None

    ride_name = ride_name.lower()

    for land in data.get("lands", []):
        for ride in land.get("rides", []):
            name = ride.get("name", "").lower()

            if ride_name in name:
                wait = ride.get("wait_time", None)
                is_open = wait is not None
                return is_open, wait

    return False, None

def fetch_calendar_html():
    try:
        r = requests.get(CALENDAR_URL, timeout=10)
        r.raise_for_status()
        return r.text
    except:
        return None


def parse_crowd_levels(html):
    """
    Extract crowd-related signals from the calendar page.
    Returns a structured RL-friendly state vector.
    """

    if html is None:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Heuristic: queue-times uses colored indicators / labels in the calendar
    # We try to capture any "crowd level" keywords or numeric hints.
    text = soup.get_text(" ").lower()

    # Common crowd descriptors (if present in page text)
    labels = {
        "very low": 0.1,
        "low": 0.25,
        "moderate": 0.5,
        "busy": 0.75,
        "very busy": 1.0
    }

    # Extract occurrences
    found_levels = []
    for label, val in labels.items():
        count = text.count(label)
        found_levels.extend([val] * count)

    # Fallback: try extracting any numeric percentages like "80%"
    percents = re.findall(r"(\d{1,3})%", text)
    percent_vals = [min(int(p) / 100.0, 1.0) for p in percents]

    all_vals = found_levels + percent_vals

    if not all_vals:
        # No signal found → neutral state
        return {
            "mean_crowd": 0.5,
            "max_crowd": 0.5,
            "min_crowd": 0.5,
            "samples": 0,
            "timestamp": datetime.utcnow().isoformat()
        }

    state = {
        "mean_crowd": sum(all_vals) / len(all_vals),
        "max_crowd": max(all_vals),
        "min_crowd": min(all_vals),
        "samples": len(all_vals),
        "timestamp": datetime.utcnow().isoformat()
    }

    return state


def get_crowd_state():
    html = fetch_calendar_html()
    crowd_state = parse_crowd_levels(html)
    return crowd_state
