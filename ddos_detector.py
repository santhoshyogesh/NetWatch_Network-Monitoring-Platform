from collections import defaultdict
import time

traffic = defaultdict(list)

def detect_ddos(src_ip):

    current = time.time()

    traffic[src_ip].append(current)

    traffic[src_ip] = [
        t for t in traffic[src_ip]
        if current - t < 10
    ]

    if len(traffic[src_ip]) > 100:

        return True

    return False