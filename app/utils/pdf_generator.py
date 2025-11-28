import os
import datetime

def generate_txt_report(giga_text, proxy_text):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if not os.path.exists("reports"):
        os.makedirs("reports")
    filename = f"reports/report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("Анализ от нейросетей\n")
        f.write("="*20 + "\n")
        f.write("GIGAChat:\n")
        f.write(giga_text + "\n\n")
        f.write("ProxyAPI:\n")
        f.write(proxy_text + "\n")

    return filename
