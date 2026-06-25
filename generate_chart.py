import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/traffic_log.csv",
    header=None,
    names=["Source","Destination","Protocol","Size"]
)

protocol_counts = df["Protocol"].value_counts()

plt.figure(figsize=(6,4))
protocol_counts.plot(kind="bar")

plt.title("Protocol Distribution")
plt.tight_layout()

plt.savefig("static/protocol_chart.png")