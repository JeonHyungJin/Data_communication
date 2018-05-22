import socket

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening...")
data,addr = server_sock.recvfrom(5000)

typed_msg = data.decode()
msg_type = typed_msg[0]
just_msg = typed_msg[1:]
final_msg=""

print("Type of Message : " + msg_type)
print("Received Message from client : " + just_msg)

if(msg_type == "0"):
	final_msg = final_msg + just_msg.upper()
if(msg_type == "1"):
	final_msg = final_msg + just_msg.lower()
if(msg_type == "2"):
	final_msg = final_msg + just_msg.swapcase()
if(msg_type == "3"):
	final_msg = final_msg + just_msg[::-1]

	
print("Converted Message : " + final_msg)
server_sock.sendto(final_msg.encode() ,addr)
print("Send message to client back..")
