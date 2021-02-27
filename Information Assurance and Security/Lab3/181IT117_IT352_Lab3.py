import binascii
from scapy.all import *

acl_rules = [["Source IP",	"Source Port",	"Destination IP",	"Destination Port",	"Action"],
            ["10.10.1.1",	"Any",	"Any",	"80",	"Deny"],
            ["Any",	"Any",	"100.100.100.100",	"80",	"Deny"],
            ["Any",	"Any",	"100.100.110.100",	"400",	"Deny"],
            ["Any",	"Any",	"200.200.200.200",	"Any",	"Deny"],
            ["Any",	"Any",	"100.102.100.102 ",	"Any",	"Deny"],
            ["Any",	"Any",	"Any",	"Any",	"Deny"]]

filter_ip = ["100.100.100.100", "100.100.110.100", "200.200.200.200", "100.102.100.102"]

def main():
    tc = int(input("Enter the Test Case Number: "))
    # ip=input("Enter IP address of Destination: ")

    print("Sniffing ...........................\n\n")

    sfilter=("dst host "+str(filter_ip[tc-1]))
    packet = sniff(filter = sfilter, count = 1)
    rawp = raw(packet[0])
    print("Raw Packet: "+"\n"+str(rawp)+"\n")
    hexp = binascii.hexlify(rawp).decode()
    temp = str(hexp)
    final = ""+temp[0]
    for i in range(1,len(temp)):
        if i%2 == 0:
            final += ' '
        final += temp[i]

    print("Packet in hexadecimal format: \n",final)

    packet_dumps = []
    packet_dumps.append(final)


    for i in range(len(packet_dumps)):
        packet_dumps[i] = packet_dumps[i].split(' ')

    cnt=1
    for dump in packet_dumps:
        # print("\n\n\t\tPACKET ",cnt)
        cnt+=1
        dest_mac = dump[0:6]
        source_mac = dump[6:12]


        ether_type = dump[12:14]
        if ether_type == ["08","00"]:

            version 		= dump[14][0]
            IHL 			= dump[14][1]
            total_length 	= dump[16:18]
            protocol 		= dump[23]
            source_ip 		= hextointarr(dump[26:30])
            dest_ip 		= hextointarr(dump[30:34])
            src_port 		= hextointnum(dump[34:36])
            dest_port 		= hextointnum(dump[36:38])

            if protocol== "11":
                print("\n\nProtocol           :UDP")
            elif protocol == "06":
                print("\n\nProtocol           :TCP")
            print("Version		   :",version)
            print("IHL		   :",IHL)
            print("\nSource MAC: {}:{}:{}:{}:{}:{}".format(source_mac[0],source_mac[1],source_mac[2],source_mac[3],source_mac[4],source_mac[5]))
            print("Destination MAC: {}:{}:{}:{}:{}:{}".format(dest_mac[0],dest_mac[1],dest_mac[2],dest_mac[3],dest_mac[4],dest_mac[5]))

            print("\nSource IP: {}.{}.{}.{}".format(source_ip[0],source_ip[1],source_ip[2],source_ip[3]))
            print("Source Port: {}".format(src_port))
            print("Destination IP: {}.{}.{}.{}".format(dest_ip[0],dest_ip[1],dest_ip[2],dest_ip[3]))
            print("Destination Port: {}".format(dest_port))
            print("\nACL Rule Applied   :",acl_rules[tc])
            if validate(tc,src_port,dest_port,source_ip,dest_ip):
                if(acl_rules[tc][-1] == "Allow"):
                    print("\n\nResult : ALLOW")
                else:
                    print("\n\nResult : DENY")
            else:
                if(acl_rules[tc][-1] == "Deny"):
                    print("\n\nResult : ALLOW")
                else:
                    print("\n\nResult : DENY")


def validate(rule_id, src_port, dest_port, src_ip, dest_ip):
    acl_src_ip = acl_rules[rule_id][0]
    acl_dest_ip = acl_rules[rule_id][1]
    acl_src_port = acl_rules[rule_id][2]
    acl_dest_port = acl_rules[rule_id][3]
    if checkIP(acl_src_ip,src_ip) and checkIP(acl_dest_ip,dest_ip) and checkPort(acl_src_port,src_port) and checkPort(acl_dest_port,dest_port):
        return True
    return False

def hextointarr(arr):
    ans = []
    for element in arr:
        temp = int(element,16)
        ans.append(temp)
    return ans

def hextointnum(arr):
    hexstring=""
    for element in arr:
        hexstring +=element
    return int(hexstring,16)

def checkIP(acl_ip,derived_ip):

    if acl_ip == "Any":
        return True

    acl_ip = acl_ip.split(".")

    for i in range(4):
        if acl_ip[i] != str(derived_ip[i]) and acl_ip[i] != "*":
            return False

    return True

def checkPort(acl_port,derived_port):
    if acl_port == str(derived_port):
        return True

    if acl_port == "Any":
        return True

    return False




if __name__ == "__main__":

    main()
