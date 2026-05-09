import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def load_raw_catalog() -> list[dict]:
    with open(BASE_DIR / "data" / "shl_product_catalog.json","r") as f:
        catalog = f.read()
        data = json.loads(catalog)
        return data
    
KEYS_TO_CODE = {
    "Ability & Aptitude": "A",
    "Knowledge & Skills": "K",
    "Personality & Behavior": "P",
    "Biodata & Situational Judgment": "B",
    "Simulations": "S",
    "Competencies": "C",
    "Development & 360": "D",
    "Assessment Exercises": "E",
}
def get_test_type(keys : list[str])-> str:
    codes = []
    for key in keys:
        code = KEYS_TO_CODE.get(key) 
        if code:
            codes.append(code)
    return ",".join(codes)


def build_embed_text(item:dict) -> str:
    name = item["name"]
    keys = " ".join(item["keys"])
    description = item["description"]
    job_levels = item["job_levels_raw"]
    languages = item["languages_raw"]

    return f"{name} | {keys} | {description} | {job_levels} | {languages}"

def get_catalog() -> list[dict]:
    items = load_raw_catalog()
    entries = []
    for item in items:
        test_type = get_test_type(item["keys"])
        embed_text = build_embed_text(item)

        entry = {
            "entity_id":item.get("entity_id"),
            "name":item.get("name"),
            "url":item.get("link"),
            "test_type":test_type,
            "keys":item.get("keys"),
            "description":item.get("description"),
            "job_levels":item.get("job_levels"),
            "duration":item.get("duration"),
            "languages":item.get("languages"),
            "remote":item.get("remote"),
            "adaptive":item.get("adaptive"),
            "embed_text":embed_text
        }
        entries.append(entry)
    return entries

if __name__ == "__main__":
    catalog = get_catalog()
    print(f"Total entries: {len(catalog)}")
    print(catalog[0])