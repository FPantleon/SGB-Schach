import requests
from bs4 import BeautifulSoup

# URL zur Mannschaftsaufstellung
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/teamPortrait?teamtable=1815599&pageState=vorrunde&championship=Ostalb+25%2F26&group=4209"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text[:1000])  # gib den Anfang des HTML aus
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle finden
tables = soup.find_all('table')
if len(tables) < 3:
    raise Exception("❌ Nicht genügend Tabellen auf der Seite gefunden.")
table = tables[2]
if not table:
    raise Exception("❌ Mannschaftstabelle nicht gefunden.")

# Alle Zeilen holen (ohne Tabellenkopf)
rows = table.find_all('tr')[1:]  # erste Zeile ist Kopf

# HTML-Grundgerüst
html_content = """
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>SG Bettringen – Mannschaftsaufstellung</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; }
    h1 { text-align: center; }
    table { border-collapse: collapse; width: 100%; background-color: #fff; }
    th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
    th { background-color: #e0e0e0; }
    tr:nth-child(even) { background-color: #f2f2f2; }
  </style>
</head>
<body>
  <h1>SG Bettringen – Mannschaftsaufstellung 2024/25</h1>
  <table>
    <tr>
      <th>Brett</th>
      <th>Name</th>
      <th>DWZ</th>
      <th>Einsätze</th>
      <th>Brettpunkte</th>
    </tr>
"""

# Zeilen extrahieren
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) >= 6:  # sicherstellen, dass genug Spalten vorhanden sind
        brett = cols[0].text.strip()
        name = cols[1].get_text(strip=True)
        dwz = cols[3].text.strip()
        einsaetze = cols[4].text.strip()
        punkte = cols[5].text.strip()

        html_content += f"""
    <tr>
      <td>{brett}</td>
      <td>{name}</td>
      <td>{dwz}</td>
      <td>{einsaetze}</td>
      <td>{punkte}</td>
    </tr>
"""


html_content += """
  </table>
</body>
</html>
"""

# Datei schreiben
with open("aufstellung.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ aufstellung.html wurde erfolgreich erstellt.")
