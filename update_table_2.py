import requests
from bs4 import BeautifulSoup

# URL der Tabelle der 2. Mannschaft
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/groupPage?championship=Ostalb+24%2F25&group=1181"
response = requests.get(url)
response.encoding = 'utf-8'

# HTML parsen
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle finden
table = soup.find('table')
if not table:
    raise Exception("❌ Tabelle nicht gefunden!")

# Alle Links aus der Tabelle entfernen
for a in table.find_all('a'):
    a.replace_with(a.get_text())

# SG Bettringen hervorheben
for row in table.find_all('tr'):
    if 'SG Bettringen' in row.get_text():
        row['style'] = 'background-color: #ffeb3b; font-weight: bold;'

# HTML-Vorlage erzeugen
html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>A-Klasse Schwäbisch Gmünd – Automatisch</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      padding: 20px;
      background-color: #f9f9f9;
    }}
    h1 {{
      text-align: center;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      background-color: #fff;
    }}
    th, td {{
      border: 1px solid #ccc;
      padding: 8px;
      text-align: center;
    }}
    th {{
      background-color: #e0e0e0;
    }}
    tr:nth-child(even) {{
      background-color: #f2f2f2;
    }}
  </style>
</head>
<body>
  <h1>A-Klasse Schwäbisch Gmünd 2024/25 – Tabelle (automatisch)</h1>
  {str(table)}
</body>
</html>
"""

# Datei schreiben
with open("bettringen2.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ bettringen2.html erfolgreich erstellt.")
