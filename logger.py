import csv

def save_packet(src, dst, protocol, size):

    with open(
        "data/traffic_log.csv",
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [src, dst, protocol, size]
        )