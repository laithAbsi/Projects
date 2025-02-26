import socket
from collections import defaultdict
import dpkt

# Ports used by the protocols we are interested in
# Source: https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
PORT_HTTP = 80
PORT_HTTPS = 443
PORT_FTP_DATA = 20
PORT_FTP_CONTROL = 21
PORT_SSH = 22
PORT_SMTP = 25
PORT_DHCP_1 = 67
PORT_DHCP_2 = 68
PORT_NTP = 123

# Constants for detecting SYN scanning
SYN_SENT_MINIMUM = 100
SYN_RECEIVED_MULTIPLIER = 5

def packet_summary(filename: str):
    """Prints hierarchically by type the number of packets seen."""
    counts = defaultdict(int)

    with open(filename, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth, dpkt.ethernet.Ethernet):
                counts['Ethernet'] += 1

                if isinstance(eth.data, dpkt.ip.IP):  # IPv4
                    ip = eth.data
                    counts['IP'] += 1  # Increment for any IP
                    counts['IPv4'] += 1

                    # Check for TCP/UDP
                    if isinstance(ip.data, dpkt.tcp.TCP):
                        tcp = ip.data
                        counts['TCP'] += 1
                        # Check protocol by port
                        if tcp.dport == PORT_HTTP or tcp.sport == PORT_HTTP:
                            counts['HTTP'] += 1
                        elif tcp.dport == PORT_HTTPS or tcp.sport == PORT_HTTPS:
                            counts['HTTPS'] += 1
                        elif tcp.dport in [PORT_FTP_DATA, PORT_FTP_CONTROL] or tcp.sport in [PORT_FTP_DATA, PORT_FTP_CONTROL]:
                            counts['FTP'] += 1
                        elif tcp.dport == PORT_SSH or tcp.sport == PORT_SSH:
                            counts['SSH'] += 1
                        elif tcp.dport == PORT_SMTP or tcp.sport == PORT_SMTP:
                            counts['SMTP'] += 1

                    elif isinstance(ip.data, dpkt.udp.UDP):
                        udp = ip.data
                        counts['UDP'] += 1
                        if udp.dport in [PORT_DHCP_1, PORT_DHCP_2] or udp.sport in [PORT_DHCP_1, PORT_DHCP_2]:
                            counts['DHCP'] += 1
                        elif udp.dport == PORT_NTP or udp.sport == PORT_NTP:
                            counts['NTP'] += 1

                elif isinstance(eth.data, dpkt.ip6.IP6):  # IPv6
                    ip6 = eth.data
                    counts['IP'] += 1  # Increment for any IP
                    counts['IPv6'] += 1

                elif isinstance(eth.data, dpkt.arp.ARP):
                    counts['ARP'] += 1

                else:
                    counts['Non-IP'] += 1

    # Print packet counts in specified order and format
    print("Packet Summary:")
    ordered_keys = ["Ethernet", "IP", "IPv4", "IPv6", "TCP", "HTTP", "HTTPS", "FTP", "SSH", "SMTP",
                    "UDP", "DHCP", "NTP", "Non-IP", "ARP"]
    for key in ordered_keys:
        if counts[key] >= 0:
            print(f"{key}: {counts[key]}")
    print()


def subnet_summary(filename: str):
    """Prints the different subnets appearing in the packets."""
    subnet_counts = defaultdict(int)

    with open(filename, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)

            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                src_ip = socket.inet_ntoa(ip.src)
                subnet = '.'.join(src_ip.split('.')[:2])
                subnet_counts[subnet] += 1

    # Sort and print subnets by count
    print("Subnet Summary:")
    for subnet, count in sorted(subnet_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{subnet}: {count}")
    print()

def detect_syn_scanning(filename: str):
    """Prints IP addresses that potentially performed SYN scans."""
    syn_counts = defaultdict(int)
    syn_ack_counts = defaultdict(int)

    with open(filename, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for timestamp, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)

            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                if isinstance(ip.data, dpkt.tcp.TCP):
                    tcp = ip.data
                    src_ip = socket.inet_ntoa(ip.src)
                    dst_ip = socket.inet_ntoa(ip.dst)

                    # Check if the SYN flag is set and ACK flag is not set
                    if (tcp.flags & dpkt.tcp.TH_SYN) and not (tcp.flags & dpkt.tcp.TH_ACK):
                        syn_counts[src_ip] += 1

                    # Check for SYN+ACK flag
                    elif (tcp.flags & dpkt.tcp.TH_SYN) and (tcp.flags & dpkt.tcp.TH_ACK):
                        syn_ack_counts[dst_ip] += 1

    # Print IPs with potential SYN scans
    print("SYN Scanners (sent, received):")
    for ip in sorted(syn_counts.keys()):
        syn_sent = syn_counts[ip]
        syn_ack_received = syn_ack_counts[ip]
        if syn_sent >= SYN_SENT_MINIMUM and syn_sent >= SYN_RECEIVED_MULTIPLIER * syn_ack_received:
            print(f"{ip} ({syn_sent}, {syn_ack_received})")
    print()


# Functions implemented. Next steps: test with provided PCAP files (if accessible).
if __name__ == "__main__":
    packet_summary("part1.pcap")
    subnet_summary("part1.pcap")
    detect_syn_scanning("part2.pcap")
