from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    status TEXT
)
""")
conn.commit()

class SensorData(BaseModel):
    temperature: float

@app.post("/sensor-data")
def receive_data(data: SensorData):
    status = "normal"

    if data.temperature > 80:
        status = "anomaly"

    cursor.execute(
        "INSERT INTO sensor_data (temperature, status) VALUES (?, ?)",
        (data.temperature, status)
    )
    conn.commit()

    return {"message": "Data received", "status": status}

@app.get("/alerts")
def get_alerts():
    cursor.execute("SELECT * FROM sensor_data WHERE status='anomaly'")
    results = cursor.fetchall()
    return {"alerts": results}
