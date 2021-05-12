# Server program for Fiat-Shamir Authentication Scheme

import socket
import math

# Code to connect to the client
host = '127.0.0.1'
port = 3003
address = (host, port)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

print ("Server is listening.....")
conn, address = server_socket.accept()
print ("Client connected ", address)

n_list = []
v_list = []

# The file server_values.txt contains values of N = p*q and v = s^2 % N
with open("server_values.txt") as file_open :
	array=file_open.read().strip().split(" ")
    
for i in range(5):
    n_list.append(array[i])
    v_list.append(array[i+5])

i = 0
for j in range(10):
    if(j==2 or j==4 or j==6 or j==8):
        i+=1
    x = conn.recv(3003).decode()
    if x == "Not in range":
                print("Secret not verified!")
                exit()
    
    x = int(x)
    print("\nReceived the witness value x from the client....")
    c = input("\nPlease enter value of the challenge bit : ")
    conn.send(c.encode())
    y = int(conn.recv(3003).decode())
    print("\nReceived the response value y from the client....")
    print("\nThe value of Y^2 is : ", y*y)

    result = x * pow(int(v_list[i]), int(c))
    print("\nThe value of X* (V^c) is : ", str(result))

    print("\nVerifying if Y^2 = X* (V^c) ")
    intr=abs(y*y-result)
    if intr==0:
        print("\n-----------RESULT: PASS-----------")
    else:
        print("\n-----------RESULT: FAIL-----------")

    

