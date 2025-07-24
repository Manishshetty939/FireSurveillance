import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="firesurv",
        user="postgres",
        password="admin123",
        cursor_factory=RealDictCursor
    )

def insert_fire_alert(status, confidence, image, latitude, longitude):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fire_alerts (status, confidence, image, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    """, (status, confidence, image, latitude, longitude))
    conn.commit()
    cur.close()
    conn.close()
    