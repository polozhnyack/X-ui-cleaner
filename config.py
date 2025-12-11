import sqlite3

DB_PATH = "/etc/x-ui/x-ui.db"


conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT value FROM settings WHERE key = 'webBasePath'")
row = cur.fetchone()

if row and row[0]:
    API_TOKEN = row[0].strip("/")
else:
    API_TOKEN = None

conn.close()
