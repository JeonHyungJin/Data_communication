import socket

print("===================================")
print("      String Change Program")
print("===================================")
print("type = 0,1,2,3")
print("===================================")

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_type = input("Input Type : ")
client_msg = input("Input your Message : ")

client_final = client_type + client_msg

clnt_sock.sendto(client_final.encode(), (serverIP, serverPort))
print("Send Message to Server..")
print("Received Message from Server : "+(clnt_sock.recv(1024)).decode())
