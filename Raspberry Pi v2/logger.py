import serial
import sqlite3
import time

# ===== SERIAL SETUP =====
ser = serial.Serial('/dev/ttyUSB0', 115200)  # Change for Windows: COM3

# ===== DATABASE SETUP =====
conn = sqlite3.connect('power.db')
c = conn.cursor()

# ===== CREATE TABLE =====
c.execute('''
CREATE TABLE IF NOT EXISTS readings (
    timestamp REAL,
    voltage REAL,
    current REAL,
    power REAL,
    energy REAL
)
''')
conn.commit()

print("Logging started...")

# ===== ENERGY VARIABLES =====
last_time = time.time()
total_energy = 0  # in Wh

# ===== MAIN LOOP =====
while True:
    try:
        line = ser.readline().decode().strip()
        print("Raw:", line)

        # Expected: V:230.5,I:0.45
        parts = line.split(',')

        voltage = float(parts[0].split(':')[1])
        current = float(parts[1].split(':')[1])

        power = voltage * current  # Watts

        current_time = time.time()
        dt = current_time - last_time
        dt_hours = dt / 3600

        energy_increment = power * dt_hours
        total_energy += energy_increment

        last_time = current_time

        # Store in DB
        c.execute(
            "INSERT INTO readings VALUES (?, ?, ?, ?, ?)",
            (current_time, voltage, current, power, total_energy)
        )
        conn.commit()

        print(f"Stored → V:{voltage} I:{current} P:{power} E:{total_energy:.4f}Wh")

    except Exception as e:
        print("Error:", e)