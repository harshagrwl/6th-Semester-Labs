# Client program for Fiat-Shamir Authentication Scheme

import socket

# Function to efficiently perform power calculations
def exp_quick(base, exponent, modulo):
    x = 1
    y = base % modulo
    b = exponent
    while (b > 0):
        if ((b % 2) == 0):  # If b is even
            y = (y * y) % modulo
            b = b / 2
        else:  # If b is odd
            x = (x * y) % modulo
            b = b - 1
    return x


# Code to connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 3003))

# The file client_values.txt contains the prime number p, prime number q and private key s

# There are 5 test cases

with open("client_values.txt") as file_open:
    array=file_open.read().strip().split(" ")

p_list = []     # List of prime numbers p
q_list = []     # List of prime numbers q
s_list = []     # List of private key values s
n_list = []     # List of N values, N = p * q
v_list = []     # List of public key values v

for i in range(len(array)):
    if(i%3==0):
        p_list.append(array[i])
        continue
    
    elif(i%3==1):
        q_list.append(array[i])
        continue
    
    else:
        s_list.append(array[i])


for i in range(5):

    print("\n\n------------------- TEST CASE #" + str(i+1) + " ------------------")

    print("\nValue of prime number p : ", p_list[i])
    print("\nValue of prime number q :", q_list[i])
    print("\nValue of the private key s :", s_list[i])

    # Calculation of value of N = p * q
    n_list.append(str(int(p_list[i]) * int(q_list[i])))
    print("\nValue of N = p * q : ", n_list[i])

    # Calculation of public key value v = s^2 % N
    v_list.append(str(exp_quick(int(s_list[i]),2,int(n_list[i]))))
    print("\nValue of public key v :", v_list[i])

    # Request for the number of rounds
    num_round = 2

    for num in range(num_round):
        print("\n--------------- ROUND #"+ str(num+1) + "---------------")
        # Request for the random number
        r = int(input("\nPlease enter the random number : "))
        if r < 0 or r >= int(n_list[i]) - 1:
            print("Error: r not in range.\n")
            client_socket.send("Not in range".encode())
            exit()

        if int(s_list[i]) < 0 or int(s_list[i]) >= int(n_list[i]) - 1:
            print("Error: s not in range.\n")
            client_socket.send("Not in range".encode())
            exit()
        # Calculation of the value of witness - 

        x= str(exp_quick(r,2,int(n_list[i])))
        print("\nValue of the witness x : ", x)

        # Sending the value of witness to the server - 
        client_socket.send(x.encode())
        print("\nSending the witness value to the server......")

        # Getting the challenge bit from the server - 
        c = int(client_socket.recv(1776).decode())
        print("\nThe challenge bit received from server is : ",c)

        # The response value y is - 
        y = str(r * exp_quick(int(s_list[i]),c,int(n_list[i])))
        print("\nThe value of the response value y is : ",y)

        # Sending the response value to server for verification - 
        client_socket.send(y.encode())
        print("\nSending the response value to server for verification......")

        
        







