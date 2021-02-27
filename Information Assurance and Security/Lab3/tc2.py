from scapy.all import *

packet=IP(src="200.200.200.200", dst="100.100.110.100")/TCP(sport=81, dport=400)

srloop(packet)