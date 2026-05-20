import scapy.all as scapy
import argparse

def scan(ip):
    arp = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    ping = broadcast/arp
    response, unresponsed = scapy.srp(ping, timeout=1)
    print(response.summary())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Network Scanner basato su richieste ARP.")
    parser.add_argument("-t", "--target", dest="target", required=True, help="IP target o subnet (es. 192.168.1.0/24)")
    options = parser.parse_args()
    
    scan(options.target)