import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# ===== CONNECT DATABASE =====
conn = sqlite3.connect('power.db')
c = conn.cursor()

# ===== FETCH DATA =====
c.execute("SELECT timestamp, voltage, current, power, energy FROM readings ORDER BY timestamp ASC")
rows = c.fetchall()

conn.close()

# ===== CHECK DATA =====
if not rows:
    print("❌ No data found in database!")
    exit()

# ===== PROCESS DATA =====
timestamps = []
voltage_values = []
current_values = []
power_values = []
energy_values = []

for row in rows:
    ts = datetime.fromtimestamp(row[0])
    timestamps.append(ts)

    voltage_values.append(row[1])
    current_values.append(row[2])
    power_values.append(row[3])
    energy_values.append(row[4])

# ===== ENERGY SUMMARY =====
total_energy_wh = energy_values[-1]
total_energy_kwh = total_energy_wh / 1000

print("\n⚡ ENERGY SUMMARY")
print(f"Total Energy: {total_energy_wh:.3f} Wh")
print(f"Total Energy: {total_energy_kwh:.5f} kWh\n")

# ===== PLOT 1: POWER =====
plt.figure()
plt.plot(timestamps, power_values, linewidth=1)

plt.xlabel("Time")
plt.ylabel("Power (W)")
plt.title("Full Power Consumption")

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("power_graph.png")

# ===== PLOT 2: ENERGY =====
plt.figure()
plt.plot(timestamps, energy_values, linewidth=2)

plt.xlabel("Time")
plt.ylabel("Energy (Wh)")
plt.title("Energy Accumulation")

plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("energy_graph.png")

# ===== SHOW ALL =====
plt.show()