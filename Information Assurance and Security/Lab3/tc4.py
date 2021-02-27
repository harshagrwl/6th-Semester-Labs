from scapy.all import *

packet=IP(src="200.20.202.20", dst="100.102.100.102")/TCP(sport=81, dport=80)

srloop(packet)