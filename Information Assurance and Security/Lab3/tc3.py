from scapy.all import *

packet=IP(src="20.20.20.20", dst="200.200.200.200")/TCP(sport=81, dport=80)

sr(packet)