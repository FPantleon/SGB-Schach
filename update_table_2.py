import requests
from bs4 import BeautifulSoup

# URL zur Tabelle SG Bettringen 2
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/groupPage?championship=Ostalb+24%2F25&group=1181"
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle suchen
table = soup.find('table')
if not table:
    raise Exception("❌ Tabelle nicht gefunden!")

# Links entfernen
for a in table.find_all('a'):
    a.replace_with(a.get_text())

# Neue HTML-Tabelle erzeugen (ohne erste Spalte)
html = "<table>\n"

# Tabellenkopf übernehmen
headers = table.find_all("tr")[0].find_all("th")
html += "  <tr>\n"
for th in headers[1:]:  # Erste Spalte überspringen
    html += f"    <th>{th.get_text(strip=True)}</th>\n"
html += "  </tr>\n"

# SG Bettringen hervorheben
for row in table.find_all("tr")[1:]:
    cols = row.find_all("td")
    if not cols:
        continue

    relevante_spalten = cols[1:]  # Erste Spalte überspringen
    verein_name = relevante_spalten[1].get_text(strip=True)

    # Hervorhebung
    if "SG Bettringen 2" in verein_name:
        html += '  <tr style="font-weight: bold; background-color: #ffeb3b;">\n'
    else:
        html += "  <tr>\n"

    for col in relevante_spalten:
        html += f"    <td>{col.get_text(strip=True)}</td>\n"
    html += "  </tr>\n"

html += "</table>"

# HTML-Seite erzeugen
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
  {html}
</body>
</html>
"""

# HTML-Datei schreiben
with open("bettringen2.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ bettringen2.html erfolgreich erstellt.")
