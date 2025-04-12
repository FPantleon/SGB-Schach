import requests
from bs4 import BeautifulSoup

# URL zur Tabelle der 2. Mannschaft
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/groupPage?championship=Ostalb+24%2F25&group=1181"
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle finden
table = soup.find('table')
if not table:
    raise Exception("❌ Tabelle nicht gefunden!")

# Links entfernen
for a in table.find_all('a'):
    a.replace_with(a.get_text())

# SG Bettringen 2 hervorheben
for row in table.find_all('tr'):
    if 'SG Bettringen' in row.get_text():
        row['style'] = 'background-color: #c3fdff; font-weight: bold;'

# HTML bauen
html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>SG Bettringen 2 – Tabelle</title>
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
  <h1>SG Bettringen 2 – Bezirksklasse Ostalb Ost 2024/25</h1>
  {str(table)}
</body>
</html>
"""

# Datei speichern
with open("bettringen2.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Tabelle wurde erfolgreich erstellt.")
