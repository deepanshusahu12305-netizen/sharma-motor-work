
import sqlite3

conn = sqlite3.connect("garage.db")

conn.execute("CREATE TABLE IF NOT EXISTS services(id INTEGER PRIMARY KEY, service TEXT, price INTEGER)")
conn.execute("CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, car TEXT, service TEXT)")

conn.commit()
conn.close()

print("Database initialized.")
