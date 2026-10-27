import functools
import json
from pathlib import Path

RATES_FILE = Path(__file__).with_name("rates.json")


@functools.lru_cache(maxsize=None)
def rate_for(region):
    """USD exchange rate for a region, read from rates.json."""
    return json.loads(RATES_FILE.read_text())[region]
