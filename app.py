from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def db():
    return sqlite3.connect("db.sqlite")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/lookup/{barcode}")
def lookup(barcode: str):
    con = db()
    cur = con.cursor()

    cur.execute("SELECT name, stellplatz, blocklager, scans FROM artikel WHERE barcode=?", (barcode,))
    row = cur.fetchone()

    if row:
        scans = row[3] + 1
        cur.execute("UPDATE artikel SET scans=? WHERE barcode=?", (scans, barcode))
        con.commit()

        return {
            "found": True,
            "name": row[0],
            "stellplatz": row[1],
            "block": bool(row[2]),
            "scans": scans
        }

    return {"found": False}

@app.post("/add")
async def add(request: Request):
    data = await request.json()

    con = db()
    cur = con.cursor()

    cur.execute("""
    INSERT INTO artikel (barcode, name, stellplatz, blocklager, scans)
    VALUES (?, ?, ?, ?, 0)
    """, (
        data["barcode"],
        data["name"],
        data["stellplatz"],
        int(data["blocklager"])
    ))

    con.commit()
    return {"ok": True}
