from scapy.all import sniff, IP, TCP, UDP
from logger import save_packet
from anomaly_detector import detect

def process_packet(packet):

    if packet.haslayer(IP):

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        protocol = "OTHER"

        if packet.haslayer(TCP):
            protocol = "TCP"

        elif packet.haslayer(UDP):
            protocol = "UDP"

        size = len(packet)

        # Save packet to CSV
        save_packet(
            src_ip,
            dst_ip,
            protocol,
            size
        )

        detect()

        print(
            f"Source: {src_ip} | Destination: {dst_ip} | Protocol: {protocol} | Size: {size}"
        )

sniff(prn=process_packet, store=False)