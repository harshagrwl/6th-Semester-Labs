from scapy.all import *

packet=IP(src="20.20.20.20", dst="100.100.100.100")/TCP(sport=11, dport=80)

sr(packet)