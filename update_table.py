import requests
from bs4 import BeautifulSoup

# URL der nuLiga-Tabelle
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/groupPage?championship=Ostalb+24%2F25&group=990"
response = requests.get(url)
response.encoding = 'utf-8'

# HTML parsen
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle finden (erste mit class 'result' oder einfach erste große Tabelle)
table = soup.find('table')

# Alle Links aus der Tabelle entfernen
for a in table.find_all('a'):
    a.replace_with(a.get_text())

# SG Bettringen hervorheben
for row in table.find_all('tr'):
    if 'SG Bettringen' in row.get_text():
        row['style'] = 'background-color: #ffeb3b; font-weight: bold;'

# HTML-Vorlage bauen
html_content = f"""
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Bezirksklasse Ostalb West – Automatisch</title>
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
  <h1>Bezirksklasse Ostalb West 2024/25 – Tabelle</h1>
  {str(table)}
</body>
</html>
"""

# Datei speichern
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
