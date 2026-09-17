from __future__ import annotations

import csv
import io


def generate_csv_report(payload: dict) -> str:
    """Create a compact CSV summary of the analysis."""
    rows = [["skill", "status", "confidence", "priority"]]
    for skill in payload.get("matched_skills", []) + payload.get("partial_skills", []) + payload.get("missing_skills", []):
        rows.append([skill.get("skill", ""), skill.get("status", ""), skill.get("confidence", ""), skill.get("priority", "")])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    return output.getvalue()
