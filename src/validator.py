import json
import requests
from jsonschema import validate, ValidationError

SCHEMA_URL = (
    "https://raw.githubusercontent.com/HUPO-PSI/mzQC/main/schema/mzqc_schema.json"
)


def load_schema_from_web() -> dict:
    try:
        response = requests.get(SCHEMA_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to load schema: {e}")


def validate_mzqc(json_str: str) -> tuple[bool, str]:
    try:
        instance = json.loads(json_str)
        schema = load_schema_from_web()
        validate(instance=instance, schema=schema)
        return True, "✔ File is valid according to the mzQC JSON schema."
    except ValidationError as ve:
        return False, f"❌ Validation failed: {ve.message}"
    except Exception as e:
        return False, f"❌ Error during validation: {e}"
