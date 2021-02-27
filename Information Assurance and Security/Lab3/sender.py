from scapy.all import *

def main():
	print("Please enter the Packet data to be sent:")
	source 	= 		input("Source IP address      : ")
	dest 	= 		input("Destination IP address : ")
	sourcep = int(	input("Source port            : "))
	destp 	= int(	input("Destination port       : "))
	temp 	= 		input("Protocol (TCP or UDP)  : ")
	eth = Ether()
	ip = IP()
	ip.src = source
	ip.dst = dest
	if temp == "TCP":
		temp1 = TCP()
		temp1.sport = sourcep
		temp1.dport = destp
	elif temp == "UDP":
		temp1 = UDP()
		temp1.sport = sourcep
		temp1.dport = destp
	else:
		print("Invalid Data. Please enter the correct packet data.")
		return
	packet = ip/temp1
	sr(packet)

if __name__ == '__main__':
	main()