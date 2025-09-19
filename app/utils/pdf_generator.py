from fpdf import FPDF
import os
import datetime


def generate_pdf_report(giga_text, proxy_text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/report_{timestamp}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Заголовок
    pdf.cell(0, 10, "Анализ от нейросетей", ln=True, align='C')
    pdf.ln(10)

    # Результат GIGAChat
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, "GIGAChat:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, giga_text)

    pdf.ln(10)

    # Результат ProxyAPI
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(0, 10, "ProxyAPI:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, proxy_text)

    if not os.path.exists("reports"):
        os.makedirs("reports")

    pdf.output(filename)
    return filename