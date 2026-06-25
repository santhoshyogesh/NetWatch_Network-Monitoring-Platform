packet_count = 0
THRESHOLD = 100

def detect():

    global packet_count

    packet_count += 1

    if packet_count == THRESHOLD:
        print("\n🚨 ALERT: High Traffic Detected! 🚨\n")