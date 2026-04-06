import serial
import sqlite3
import time

# ===== SERIAL SETUP =====
ser = serial.Serial('/dev/ttyUSB0', 115200)

# ===== DATABASE SETUP =====
conn = sqlite3.connect('power.db')
c = conn.cursor()

# ===== CREATE TABLE =====
c.execute('''
CREATE TABLE IF NOT EXISTS readings (
    timestamp REAL,
    voltage REAL,
    current REAL,
    power REAL
)
''')
conn.commit()

print("Logging started...")

# ===== MAIN LOOP =====
while True:
    try:
        # Read serial data
        line = ser.readline().decode().strip()
        print("Raw:", line)

        # Parse data (expected format: V:xxx,I:xxx)
        parts = line.split(',')

        voltage = float(parts[0].split(':')[1])
        current = float(parts[1].split(':')[1])

        # Calculate power
        power = voltage * current

        timestamp = time.time()

        # Store in database
        c.execute(
            "INSERT INTO readings VALUES (?, ?, ?, ?)",
            (timestamp, voltage, current, power)
        )
        conn.commit()

        print(f"Stored → V:{voltage} I:{current} P:{power}")

    except Exception as e:
        print("Error:", e)