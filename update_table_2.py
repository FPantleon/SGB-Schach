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

# SG Bettringen hervorheben
for row in table.find_all("tr")[1:]:
    cols = row.find_all("td")
    if not cols:
        continue

    # Spalten 1 bis N überspringen die erste leere Spalte (Index 0)
    relevante_spalten = cols[1:]  # Index 1 bis Ende

    # Dann z. B. weiter mit:
    html += "<tr>\n"
    for col in relevante_spalten:
        html += f"  <td>{col.get_text(strip=True)}</td>\n"
    html += "</tr>\n"
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
  {str(table)}
</body>
</html>
"""

# HTML-Datei schreiben
with open("bettringen2.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ bettringen2.html erfolgreich erstellt.")
