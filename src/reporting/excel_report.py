from __future__ import annotations

from io import BytesIO

from openpyxl import Workbook


def generate_excel_report(payload: dict) -> bytes:
    """Generate an Excel workbook summary for the analysis."""
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Analysis"
    sheet.append(["Metric", "Value"])
    sheet.append(["Overall Match %", payload.get("overall_match_percentage", 0)])
    sheet.append(["Matched Skills", payload.get("matched_count", 0)])
    sheet.append(["Partial Skills", payload.get("partial_count", 0)])
    sheet.append(["Missing Skills", payload.get("missing_count", 0)])
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()
