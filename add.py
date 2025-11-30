import sqlite3

# Datenbank-Datei
DB = "db.sqlite"

# Artikel-Daten
barcode = "4017074133011"   # Beispiel-Barcode für "Apodis Medium PET 1L" (bitte echten Barcode einsetzen)
name = "Apodis Medium PET 1L"
stellplatz = "4191"

# Verbindung öffnen
conn = sqlite3.connect(DB)
c = conn.cursor()

# Artikel einfügen
c.execute("INSERT INTO artikel (barcode, name, stellplatz) VALUES (?, ?, ?)",
          (barcode, name, stellplatz))

conn.commit()
conn.close()

print(f"{name} erfolgreich hinzugefügt!")
