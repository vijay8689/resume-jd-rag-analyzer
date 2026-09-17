from __future__ import annotations

import json


def generate_json_report(payload: dict) -> str:
    """Serialize a structured analysis payload to JSON."""
    return json.dumps(payload, indent=2, ensure_ascii=False)
