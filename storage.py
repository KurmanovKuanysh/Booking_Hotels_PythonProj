import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
HOTELS_PATH = DATA_DIR / "hotels.json"

class Storage:
    def load_hotels(self):
        return []