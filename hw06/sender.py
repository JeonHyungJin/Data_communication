import os
import socket

serverIP = '127.0.0.1'
serverPort = 2345

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt_sock.connect((serverIP, serverPort))
print("Connect to Server...")

print("Receiver IP = " + serverIP)
print("Receiver Port = " + str(serverPort))
input_file_name = input("Input File Name : ")
input_file_name_eleven = input_file_name.ljust(11)

file_size = os.path.getsize(input_file_name)

first_send_check = '0' 
other_send_check = '1'

first_send_msg = first_send_check.encode() + input_file_name_eleven.encode() + file_size.to_bytes(4,byteorder = "big")

clnt_sock.send(first_send_msg)	#처음 메세지 보내기

count_size = 0

file = open(input_file_name, "rb")

while count_size < file_size:
	
	data = file.read(1024)	#바이트로 반환

	second_send_msg = other_send_check.encode() + input_file_name_eleven.encode() + file_size.to_bytes(4, byteorder = 'big')

	encoded_msg = second_send_msg + data

	clnt_sock.send(encoded_msg)

	print(clnt_sock.recv(1024).decode('utf-8'))

	count_size = count_size + len(data)

	if(count_size == file_size):
		print(clnt_sock.recv(1024).decode('utf-8'))

file.close()
print("File Send End.")
