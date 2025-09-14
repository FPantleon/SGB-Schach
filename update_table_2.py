import requests
from bs4 import BeautifulSoup

# URL zur Tabelle der 2. Mannschaft
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/groupPage?championship=Ostalb+25%2F26&group=4186"
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle finden
table = soup.find('table')
if not table:
    raise Exception("❌ Tabelle nicht gefunden!")

# Alle Links entfernen
for a in table.find_all('a'):
    a.replace_with(a.get_text())

# Neue HTML-Tabelle erzeugen
html = "<table>\n"

# Tabellenkopf übernehmen (erste Spalte überspringen)
headers = table.find_all("tr")[0].find_all("th")
html += "  <tr>\n"
for th in headers[1:]:
    text = th.get_text(strip=True)
    if text == "Sp":
        text = "Spiele"  # Spalte umbenennen
    html += f"    <th>{text}</th>\n"
html += "  </tr>\n"

# Tabellenzeilen übernehmen
for row in table.find_all("tr")[1:]:
    cols = row.find_all("td")
    if not cols:
        continue

    relevante_spalten = cols[1:]  # erste (leere) Spalte entfernen
    verein_name = relevante_spalten[1].get_text(strip=True).lower()  # Spalte 1 = Mannschaft

    if "bettringen" in verein_name:
        html += '  <tr style="font-weight: bold; background-color: #ffeb3b;">\n'
    else:
        html += "  <tr>\n"

    for col in relevante_spalten:
        html += f"    <td>{col.get_text(strip=True)}</td>\n"
    html += "  </tr>\n"

html += "</table>"

# HTML-Rahmen erstellen
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
  <h1>A-Klasse Schwäbisch Gmünd 2024/25 – Tabelle</h1>
  {html}
</body>
</html>
"""

# Datei speichern
with open("bettringen2.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ bettringen2.html erfolgreich erstellt.")

