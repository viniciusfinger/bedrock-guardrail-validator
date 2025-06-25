from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import json
import os

OUTPUT_JSON_PATH = "output.json"
PDF_REPORT = "guardrail_report.pdf"

def generate_report():
    if not os.path.exists(OUTPUT_JSON_PATH):
        print(f"File {OUTPUT_JSON_PATH} not found.")
        return

    with open(OUTPUT_JSON_PATH, "r", encoding="utf-8") as f:
        results = json.load(f)

    total = len([r for r in results if r["filtered_by_guardrail"] is not None])
    hits = sum(1 for r in results if r["filtered_by_guardrail"] == r["should_filter"] and r["filtered_by_guardrail"] is not None)
    accuracy = (hits / total) if total > 0 else 0

    errors = [r for r in results if r["filtered_by_guardrail"] != r["should_filter"] and r["filtered_by_guardrail"] is not None]

    doc = SimpleDocTemplate(PDF_REPORT, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("<b>Guardrail Validation Report</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 20))

    summary = (
        f"<b>Total inputs processed:</b> {total}<br/>"
        f"<b>Guardrail hits:</b> {hits}<br/>"
        f"<b>Accuracy:</b> {accuracy:.2%}"
    )
    elements.append(Paragraph(summary, styles["Normal"]))
    elements.append(Spacer(1, 20))

    if errors:
        elements.append(Paragraph("<b>Inputs not filtered correctly:</b>", styles["Heading2"]))
        data = [["Message", "Should filter?", "Filtered by guardrail?"]]
        for error in errors:
            data.append([
                error["message"],
                str(error["should_filter"]),
                str(error["filtered_by_guardrail"]),
            ])
        table = Table(data, colWidths=[250, 100, 120])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("<b>All inputs were filtered correctly!</b>", styles["Normal"]))

    doc.build(elements)
    print(f"Report generated at: {PDF_REPORT}")

if __name__ == "__main__":
    generate_report()
