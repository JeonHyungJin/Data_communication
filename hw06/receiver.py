#server의 역할
import socket
import os
import struct

ip_address = '127.0.0.1'
port_number = 2345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening...")
server_sock.listen()

client_sock,addr = server_sock.accept()

first_received_msg = client_sock.recv(16)	#처음 메세지 받기

file_name = first_received_msg[1:12].decode()
file_size = struct.unpack("!i", first_received_msg[12:16])[0]

print("File Name = " + file_name)
print("File Size = " + str(file_size))

print("File Path = ./received_dir/" + file_name)

file = open("./received_dir/" + file_name, "wb")

count_size = 0
file_path = './received_dir/' + file_name

while count_size < file_size:
	
	second_received_msg = client_sock.recv(1040)

	data = second_received_msg[16:]
		
	size_msg = '( current size / total size ) = ' + str(count_size) +'/'+ str(file_size) + ' , ' + str(round((count_size / file_size), 5) * 100) + '%'
	print(size_msg)

	file.write(data)
	
	client_sock.send(size_msg.encode())

	count_size = count_size + len(data)

	if(count_size == file_size):
		size_msg = '( current size / total size ) = ' + str(count_size) +'/'+ str(file_size) + ' , ' + str(round((count_size / file_size), 5) * 100) + '%'
		print(size_msg)
		client_sock.send(size_msg.encode())

file.close()
print("File Receive End.")

