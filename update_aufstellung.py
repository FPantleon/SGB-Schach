import requests
from bs4 import BeautifulSoup

# URL zur Mannschaftsaufstellung
url = "https://svw-schach.liga.nu/cgi-bin/WebObjects/nuLigaSCHACHDE.woa/wa/teamPortrait?teamtable=1809461&pageState=vorrunde&championship=Ostalb+24%2F25&group=990"

response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

# Tabelle finden
table = soup.find('table', class_='standard')
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
for row in rows:
    cols = row.find_all('td')
    if len(cols) >= 5:
        brett = cols[0].text.strip()
        name = cols[1].get_text(strip=True)  # Link entfernen
        dwz = cols[2].text.strip()
        einsaetze = cols[3].text.strip()
        punkte = cols[4].text.strip()

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
