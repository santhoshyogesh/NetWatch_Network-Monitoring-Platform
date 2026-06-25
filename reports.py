import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/traffic_log.csv",
    header=None,
    names=["Source", "Destination", "Protocol", "Size"]
)

top_ips = df["Source"].value_counts().head(10)

print(top_ips)

top_ips.plot(kind="bar")

plt.title("Top Source IPs")
plt.xlabel("IP Address")
plt.ylabel("Packet Count")

plt.show()