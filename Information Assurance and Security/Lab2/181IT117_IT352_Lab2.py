

# Function to validate the Port Number
def checkPort(acl_port,derived_port):
    if acl_port == str(derived_port):
        return True

    if acl_port == "Any":
        return True

    return False

# Function to validate thr IP Address
def checkIP(acl_ip,derived_ip):

    if acl_ip == "Any":
        return True

    acl_ip = acl_ip.split(".")

    for i in range(4):
        if acl_ip[i] != str(derived_ip[i]) and acl_ip[i] != "*":
            return False

    return True

# Function to convert Hexadecimal array to Integer Array
def hexToIntArray(arr):
    ans = []
    for element in arr:
        temp = int(element,16)
        ans.append(temp)
    return ans

# Function to convert hexadecimal array to Integer
def hexToInt(arr):
    hexstring=""
    for element in arr:
        hexstring +=element
    return int(hexstring,16)




def validateRule(rule,src_port,dest_port,source_ip,dest_ip):
    acl_src_ip = rule[0]
    acl_dest_ip = rule[2]
    acl_src_port = rule[1]
    acl_dest_port = rule[3]

    if rule[-1] == "Allow":
        
        if checkIP(acl_src_ip,source_ip) and checkIP(acl_dest_ip,dest_ip) and checkPort(acl_src_port,src_port) and checkPort(acl_dest_port,dest_port):
                return True 
        else:
            return False

    if rule[-1] == "Deny":
        
        if checkIP(acl_src_ip,source_ip) and checkIP(acl_dest_ip,dest_ip) and checkPort(acl_src_port,src_port) and checkPort(acl_dest_port,dest_port):
                
                return False 
        else:
            return True

# def valAllRules(src_port,dest_port,source_ip,dest_ip):
#     for rule in acl_conditions:
#         if validateRule(rule,src_port,dest_port,source_ip,dest_ip) == True:
#             return True
#     return False

# Taking the testcase file as input
input_file = open("testcases.txt","r")
ethernet_frames = [] #Initializing list of ethernet frames


# Reading the textfile and populating the list
for line in input_file:
    line = line.replace('\r',"")
    if line != "\n":
        ethernet_frames.append(line[:-1])
input_file.close()

raw_frames = ethernet_frames
for i in range(len(ethernet_frames)):
    ethernet_frames[i] = ethernet_frames[i].split(' ')


# Defining the ACL Conditions given
acl_conditions = [["Source IP", "Source Port",  "Destination IP",   "Destination Port", "Action"],
["10.100.54.*", "Any",  "Any",  "Any",  "Allow"],
["Any", "Any",  "Any",  "80",   "Deny"],
["Any", "Any",  "10.100.53.1",  "443",  "Deny"],
["Any", "Any",  "10.100.54.*",  "Any",  "Deny"],
["Any", "Any",  "Any",  "Any",  "Deny"]]


# Enumerating the individual ethernet frames 
for idx,frame in enumerate(ethernet_frames):
    print("\n\n--------------------------Testcase #",idx+1,"--------------------------\n\n")
    # print("Ethernet Frame:", raw_frames[idx])
    ether_type = frame[12:14]
    if ether_type == ["08","00"]: # IPv4 Packet

        version = frame[14][0]
        IHL = frame[14][1] #Number of 32-bit words in the header (how many 4 bytes)
        total_length = frame[16:18]
        protocol = frame[23] 
        source_ip = frame[26:30]
        dest_ip = frame[30:34]
        src_port = frame[34:36]
        dest_port = frame[36:38]
        source_mac = frame[6:12]
        dest_mac = frame[0:6]
    
    

        src_ip_dec = hexToIntArray(source_ip)
        dest_ip_dec = hexToIntArray(dest_ip)
        print("Version: {}".format(int(version,10)))
        print("Protocol: {}".format(protocol))

        print("\nSource MAC: {}:{}:{}:{}:{}:{}".format(source_mac[0],source_mac[1],source_mac[2],source_mac[3],source_mac[4],source_mac[5]))
        print("Destination MAC: {}:{}:{}:{}:{}:{}".format(dest_mac[0],dest_mac[1],dest_mac[2],dest_mac[3],dest_mac[4],dest_mac[5]))

        print("\nSource IP: {}.{}.{}.{}".format(src_ip_dec[0],src_ip_dec[1],src_ip_dec[2],src_ip_dec[3]))
        print("Source Port: {}".format(hexToInt(src_port)))
        print("Destination IP: {}.{}.{}.{}".format(dest_ip_dec[0],dest_ip_dec[1],dest_ip_dec[2],dest_ip_dec[3]))
        print("Destination Port: {}".format(hexToInt(dest_port)))
        
        print("ACL Rule Applied: ",acl_conditions[idx+1])

        if validateRule(acl_conditions[idx+1],src_port,dest_port,source_ip,dest_ip):
            print("\n\nResult: ALLOW\n")
        else:
            print("\n\nResult: DENY\n")
    else:
        print("Error. Given Ethernet frame is not valid.")

