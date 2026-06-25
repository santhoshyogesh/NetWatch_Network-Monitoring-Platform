from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER

import pandas as pd
from datetime import datetime


# ==========================================
# HEADER & FOOTER
# ==========================================

def add_header_footer(canvas, doc):
    canvas.saveState()

    # Header
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(
        40,
        810,
        "NETWATCH NETWORK SECURITY REPORT"
    )

    # Footer
    canvas.setFont("Helvetica", 9)

    canvas.drawString(
        40,
        20,
        "NetWatch v1.0 | Network Monitoring & Threat Detection"
    )

    canvas.drawRightString(
        550,
        20,
        f"Page {canvas.getPageNumber()}"
    )

    canvas.restoreState()


# ==========================================
# PDF SETUP
# ==========================================

pdf = SimpleDocTemplate(
    "NetWatch_Report.pdf"
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    textColor=colors.darkblue,
    fontSize=28
)

section_style = ParagraphStyle(
    "SectionStyle",
    parent=styles["Heading1"],
    textColor=colors.white,
    backColor=colors.darkblue,
    leftIndent=5,
    spaceBefore=10,
    spaceAfter=10
)

alert_style = ParagraphStyle(
    "AlertStyle",
    parent=styles["Normal"],
    textColor=colors.red,
    fontName="Helvetica-Bold"
)

content = []

# ==========================================
# COVER PAGE
# ==========================================

content.append(Spacer(1, 250))
content.append(
    Paragraph("NETWATCH", title_style)
)

content.append(
    Paragraph(
        "Network Security Monitoring Report",
        ParagraphStyle(
            "sub",
            parent=styles["Heading2"],
            alignment=TA_CENTER
        )
    )
)

content.append(
    Paragraph(
        f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}",
        ParagraphStyle(
            "date",
            parent=styles["Normal"],
            alignment=TA_CENTER
        )
    )
)

content.append(Spacer(1, 40))

content.append(
    Paragraph(
        "Real-Time Network Monitoring & Threat Detection Platform",
        ParagraphStyle(
            "footer",
            parent=styles["Italic"],
            alignment=TA_CENTER
        )
    )
)

content.append(PageBreak())

# ==========================================
# LOAD TRAFFIC DATA
# ==========================================

df = pd.read_csv(
    "data/traffic_log.csv",
    header=None,
    names=[
        "Source",
        "Destination",
        "Protocol",
        "Size"
    ]
)

total_packets = len(df)

tcp_count = len(
    df[df["Protocol"] == "TCP"]
)

udp_count = len(
    df[df["Protocol"] == "UDP"]
)

icmp_count = len(
    df[df["Protocol"] == "ICMP"]
)

# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

content.append(
    Paragraph(
        "Executive Summary",
        section_style
    )
)

summary_data = [
    ["Metric", "Value"],
    ["Total Packets", str(total_packets)],
    ["TCP Packets", str(tcp_count)],
    ["UDP Packets", str(udp_count)],
    ["ICMP Packets", str(icmp_count)]
]

summary_table = Table(
    summary_data,
    colWidths=[250, 150]
)

summary_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ROWBACKGROUNDS",
         (0, 1),
         (-1, -1),
         [colors.whitesmoke, colors.lightgrey])
    ])
)

content.append(summary_table)
content.append(Spacer(1, 20))

# ==========================================
# PROTOCOL STATISTICS
# ==========================================

content.append(
    Paragraph(
        "Protocol Statistics",
        section_style
    )
)

protocols = df["Protocol"].value_counts()

protocol_table_data = [
    ["Protocol", "Count"]
]

for protocol, count in protocols.items():
    protocol_table_data.append(
        [protocol, str(count)]
    )

protocol_table = Table(
    protocol_table_data,
    colWidths=[200, 150]
)

protocol_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ROWBACKGROUNDS",
         (0, 1),
         (-1, -1),
         [colors.whitesmoke, colors.lightgrey]),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ])
)

content.append(protocol_table)
content.append(Spacer(1, 20))

# ==========================================
# TOP SOURCE IPS
# ==========================================

content.append(
    Paragraph(
        "Top Source IP Addresses",
        section_style
    )
)

top_source = (
    df["Source"]
    .value_counts()
    .head(5)
)

source_data = [
    ["IP Address", "Packets"]
]

for ip, count in top_source.items():
    source_data.append(
        [ip, str(count)]
    )

source_table = Table(
    source_data,
    colWidths=[250, 120]
)

source_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ROWBACKGROUNDS",
         (0, 1),
         (-1, -1),
         [colors.whitesmoke, colors.lightgrey])
    ])
)

content.append(source_table)
content.append(Spacer(1, 20))

# ==========================================
# TOP DESTINATION IPS
# ==========================================

content.append(
    Paragraph(
        "Top Destination IP Addresses",
        section_style
    )
)

top_dest = (
    df["Destination"]
    .value_counts()
    .head(5)
)

dest_data = [
    ["IP Address", "Packets"]
]

for ip, count in top_dest.items():
    dest_data.append(
        [ip, str(count)]
    )

dest_table = Table(
    dest_data,
    colWidths=[250, 120]
)

dest_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ROWBACKGROUNDS",
         (0, 1),
         (-1, -1),
         [colors.whitesmoke, colors.lightgrey])
    ])
)

content.append(dest_table)
content.append(Spacer(1, 20))

# ==========================================
# SECURITY ALERTS
# ==========================================

content.append(
    Paragraph(
        "Security Alerts",
        section_style
    )
)

try:

    with open(
        "data/alerts.txt",
        "r"
    ) as file:

        alerts = file.readlines()

    if alerts:

        for alert in alerts[-10:]:

            content.append(
                Paragraph(
                    "⚠ " + alert.strip(),
                    alert_style
                )
            )

    else:

        content.append(
            Paragraph(
                "No Security Alerts Detected",
                styles["Normal"]
            )
        )

except FileNotFoundError:

    content.append(
        Paragraph(
            "Alert file not found.",
            styles["Normal"]
        )
    )

content.append(Spacer(1, 20))

# ==========================================
# RECOMMENDATIONS
# ==========================================

content.append(
    Paragraph(
        "Security Recommendations",
        section_style
    )
)

recommendations = [
    "Monitor unusual traffic spikes.",
    "Investigate repeated access from unknown IP addresses.",
    "Enable firewall logging and intrusion detection.",
    "Review high-volume source and destination hosts.",
    "Maintain regular network audits."
]

for item in recommendations:
    content.append(
        Paragraph(
            "• " + item,
            styles["Normal"]
        )
    )

content.append(Spacer(1, 20))

# ==========================================
# FINAL NOTE
# ==========================================

content.append(
    Paragraph(
        "End of NetWatch Security Report",
        styles["Italic"]
    )
)

# ==========================================
# GENERATE PDF
# ==========================================

pdf.build(
    content,
    onFirstPage=add_header_footer,
    onLaterPages=add_header_footer
)

print(
    "Professional NetWatch PDF Report Generated Successfully!"
)

