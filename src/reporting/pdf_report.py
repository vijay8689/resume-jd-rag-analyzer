from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_pdf_report(payload: dict) -> bytes:
    """Generate a basic PDF summary for the analysis."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Resume Analysis Report")
    pdf.drawString(50, 750, "Resume AI Match Analyzer")
    pdf.drawString(50, 730, f"Overall Match: {payload.get('overall_match_percentage', 0):.1f}%")
    pdf.drawString(50, 710, f"Matched Skills: {payload.get('matched_count', 0)}")
    pdf.drawString(50, 690, f"Partial Skills: {payload.get('partial_count', 0)}")
    pdf.drawString(50, 670, f"Missing Skills: {payload.get('missing_count', 0)}")
    pdf.save()
    return buffer.getvalue()
