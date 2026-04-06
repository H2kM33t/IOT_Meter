from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Get latest data
@app.route('/data')
def get_data():
    conn = sqlite3.connect('power.db')
    c = conn.cursor()

    c.execute("SELECT voltage, current, power FROM readings ORDER BY timestamp DESC LIMIT 1")
    row = c.fetchone()

    conn.close()

    if row:
        return jsonify({
            "voltage": row[0],
            "current": row[1],
            "power": row[2]
        })
    else:
        return jsonify({"voltage": 0, "current": 0, "power": 0})


# Get last 50 readings (for graph)
@app.route('/history')
def get_history():
    conn = sqlite3.connect('power.db')
    c = conn.cursor()

    c.execute("SELECT timestamp, power FROM readings ORDER BY timestamp DESC LIMIT 50")
    rows = c.fetchall()
    conn.close()

    rows.reverse()
    return jsonify(rows)


# Dashboard page
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)