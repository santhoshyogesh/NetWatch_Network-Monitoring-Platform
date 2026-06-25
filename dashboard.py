from flask import Flask, render_template_string, request, redirect, session
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "netwatch_secret_key"

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>NetWatch Login</title>

<style>
body{
    font-family:Arial;
    background:#0f172a;
    color:white;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.login-box{
    background:#1e293b;
    padding:30px;
    border-radius:15px;
    width:350px;
}

input{
    width:100%;
    padding:10px;
    margin:10px 0;
}

button{
    width:100%;
    padding:10px;
}
</style>

</head>

<body>

<div class="login-box">

<h2>NetWatch Login</h2>

<form method="POST">

<input
type="text"
name="username"
placeholder="Username"
required>

<input
type="password"
name="password"
placeholder="Password"
required>

<button type="submit">
Login
</button>

</form>

</div>

</body>
</html>
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <title>NetWatch Dashboard</title>

    <meta http-equiv="refresh" content="5">

    <style>

    body{
        font-family: Arial, sans-serif;
        background:linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #0f172a
    );
        color:white;
        margin:0;
        padding:0;
    }

    .header{
    position:relative;
    background:#1e293b;
    text-align:center;
    padding:25px;
    font-size:32px;
    font-weight:bold;
    box-shadow:0px 2px 10px rgba(0,0,0,0.5);
    }

    .container{
        display:flex;
        flex-wrap:wrap;
        justify-content:center;
        margin-top:20px;
    }

    .card{
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        border:1px solid rgba(255,255,255,0.1);
        width:320px;
        margin:15px;
        padding:20px;
        border-radius:15px;
        box-shadow:0px 0px 15px rgba(56,189,248,0.3);
    }

    .card h2{
        color:#38bdf8;
        margin-top:0;
    }

    .card h1{
        text-align:center;
    }

    ul{
        padding-left:20px;
    }

    li{
        margin:8px 0;
    }

    .alert{
        color:red;
        font-size:22px;
        font-weight:bold;
    }

    .normal{
        color:lightgreen;
        font-size:22px;
        font-weight:bold;
    }

    .footer{
        text-align:center;
        color:gray;
        margin-top:20px;
        padding:15px;
    }

    </style>

</head>

<script>

document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById('protocolChart');

    new Chart(ctx, {
        type: 'bar',

        data: {
            labels: {{ labels | tojson }},
            datasets: [{
                label: 'Packets',
                data: {{ values | tojson }},
                borderWidth: 1
            }]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        color: 'white'
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: 'white'
                    }
                },

                y: {
                    ticks: {
                        color: 'white'
                    }
                }
            }
        }
    });

});

</script>


<body>

<div class="header">
<a href="/download-report"
style="
position:absolute;
left:20px;
top:22px;
background:#38bdf8;
padding:8px 12px;
color:black;
text-decoration:none;
border-radius:6px;
font-size:14px;
font-weight:bold;
">
📄 PDF
</a>
🛡 NetWatch Network Monitoring Dashboard <a href="/logout"
style="
float:right;
color:white;
text-decoration:none;
font-size:18px;
">
Logout
</a>
</div>

<div class="container">

    <div class="card">
        <h2>Total Packets</h2>
        <h1>{{ total_packets }}</h1>
    </div>

    <div class="card">
        <h2>Current Time</h2>
        <h3>{{ current_time }}</h3>
    </div>

    <div class="card">
        <h2>Network Status</h2>
        <h3>{{ network_status }}</h3>
    </div>

    <div class="card">
        <h2>Alert Counter</h2>
        <h1>{{ alert_count }}</h1>
    </div>

    <div class="card">
        <h2>Protocol Usage</h2>
        <p>TCP : {{ tcp_percent }}%</p>
        <p>UDP : {{ udp_percent }}%</p>
    </div>

    <div class="card">
        <h2>Protocol Statistics</h2>

        <ul>
        {% for protocol, count in protocols.items() %}
            <li>{{ protocol }} : {{ count }}</li>
        {% endfor %}
        </ul>

    </div>

    <div class="card">
    <h2>Recent Security Alerts</h2>

    <ul>
    {% for alert_item in alerts %}
        <li>{{ alert_item }}</li>
    {% endfor %}
    </ul>

    </div>

    <div class="card">
        <h2>Top Source IPs</h2>

        <ul>
        {% for ip, count in top_ips.items() %}
            <li>{{ ip }} : {{ count }}</li>
        {% endfor %}
        </ul>

    </div>

    <div class="card">
    <h2>Packet Statistics</h2>

    <p>Average Size: {{ avg_packet_size }} Bytes</p>
    <p>Maximum Size: {{ max_packet_size }} Bytes</p>

    </div>

    <div class="card">
        <h2>Alert Status</h2>

        {% if "High Traffic" in alert %}
            <p class="alert">{{ alert }}</p>
        {% else %}
            <p class="normal">{{ alert }}</p>
        {% endif %}

    </div>

    <div class="card">
    <h2>Top Destination IPs</h2>

    <ul>
    {% for ip, count in top_destinations.items() %}
        <li>{{ ip }} : {{ count }}</li>
    {% endfor %}
    </ul>

</div>

<div class="card" style="width:700px;">
    <h2>Protocol Distribution Chart</h2>

    <canvas id="protocolChart"></canvas>
</div>

</div>

<div class="footer">

<div class="footer">
NetWatch v1.0 | Real-Time Network Traffic Monitoring System
</div>

</body>
</html>
"""

USERNAME = "admin"
PASSWORD = "netwatch123"

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True

            return redirect("/")

    return render_template_string(LOGIN_HTML)

from flask import send_file

@app.route("/download-report")
def download_report():

    if not session.get("logged_in"):
        return redirect("/login")

    return send_file(
        "NetWatch_Report.pdf",
        as_attachment=True
    )

@app.route("/")
def home():

    if not session.get("logged_in"):
        return redirect("/login")

    if not os.path.exists("data/traffic_log.csv"):
        return "<h2>No traffic data available. Run packet_sniffer.py first.</h2>"
    
    alerts = []

    if os.path.exists("data/alerts.txt"):
        with open("data/alerts.txt", "r") as file:
            alerts = file.readlines()[-5:]

    try:

        df = pd.read_csv(
            "data/traffic_log.csv",
            header=None,
            names=["Source", "Destination", "Protocol", "Size"]
        )

        protocols = df["Protocol"].value_counts().to_dict()

        labels = list(protocols.keys())
        values = list(protocols.values())

        total_packets = len(df)

        top_ips = df["Source"].value_counts().head(5).to_dict()

        top_destinations = df["Destination"].value_counts().head(5).to_dict()

        avg_packet_size = round(df["Size"].mean(), 2)
        max_packet_size = df["Size"].max()

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        tcp_count = protocols.get("TCP", 0)
        udp_count = protocols.get("UDP", 0)

        if total_packets > 0:
            tcp_percent = round((tcp_count / total_packets) * 100, 2)
            udp_percent = round((udp_count / total_packets) * 100, 2)
        else:
            tcp_percent = 0
            udp_percent = 0

        network_status = "🟢 ONLINE"

        alert_count = 0
        alert = "Normal Traffic"

        if total_packets > 100:
            alert = "🚨 High Traffic Detected"
            alert_count = 1

        return render_template_string(
    HTML,
    total_packets=total_packets,
    current_time=current_time,
    network_status=network_status,
    alert_count=alert_count,
    tcp_percent=tcp_percent,
    udp_percent=udp_percent,
    protocols=protocols,
    top_ips=top_ips,
    top_destinations=top_destinations,
    alerts=alerts,
    avg_packet_size=avg_packet_size,
    max_packet_size=max_packet_size,
    labels=labels,
    values=values,
)

    except Exception as e:
        return f"<h2>Error: {e}</h2>"
    
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)