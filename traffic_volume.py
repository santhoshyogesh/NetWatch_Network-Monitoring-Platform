import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/traffic_log.csv",
    header=None,
    names=["Source", "Destination", "Protocol", "Size"]
)

df["Size"].plot()

plt.title("Traffic Volume")
plt.xlabel("Packet Number")
plt.ylabel("Packet Size")

plt.show()