#서버
import socket
import hashlib
import struct
import time

ip_address = '127.0.0.1'
port_number = 3333

seq_num_arr = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]		#seq_num은 0~7 사용
ACK_arr = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
receiver_index = 0

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

data, addr = server_sock.recvfrom(1045)
file_info_checksum = data[0:20]
seq_ack = data[20:21]
unhash_file_info = data[20:]
hashing_info = hashlib.sha1()
hashing_info.update(unhash_file_info)
hashed_info = hashing_info.digest()

if(file_info_checksum == hashed_info):
	server_sock.sendto(seq_ack, addr)
	file_size = struct.unpack("!i", data[21:25])[0]	#앞의 4바이트 부분은 파일의 사이즈가 저장된 부분
	file_name = data[25:].decode()	#파일의 이름

print("file Name = " + file_name)
print("file Size = " + str(file_size))
print("File Path = ./received_dir/" + file_name)

file = open("./received_dir/" + file_name, "wb")

count_size = 0

while True:
	data, addr = server_sock.recvfrom(1045)
	checksum = data[0:20]
	unhash_data = data[20:]
	seq_ack = data[20:21]
	file_data=data[21:]
	hashing_data = hashlib.sha1()
	hashing_data.update(unhash_data)
	hashed_data = hashing_data.digest()

	if(checksum == hashed_data):
		file.write(file_data)
		server_sock.sendto(seq_ack, addr)
		count_size += len(data)

	if(count_size >= file_size):
		break
	
	
	
		
print("File Received End.")

