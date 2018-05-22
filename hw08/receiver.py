#서버
import socket
import hashlib
import struct
import time

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Send file info ACK...")
ACK = 0	#ACK


data, addr = server_sock.recvfrom(2000)	#처음에 파일의 정보를 읽어옴
time.sleep(5)	#파일 정보를 보낼때 timeout 체크를 위해서 sleep

file_info_checksum = data[0:20]
unhash_file_info = data[20:]
hashing_info = hashlib.sha1()
hashing_info.update(unhash_file_info)
hashed_info = hashing_info.digest()

if(file_info_checksum == hashed_info):
	ACK = (ACK + 1) % 2
	server_sock.sendto(ACK.to_bytes(4, byteorder = "big"), addr)

	file_size = struct.unpack("!i", data[21:25])[0]	#앞의 4바이트 부분은 파일의 사이즈가 저장된 부분
	file_name = data[25:].decode()	#파일의 이름
else:
	print(" * Packet corrupted!! *** - Send To Sender NAK(2)")
	NAK = 2
	server_sock.sendto(NAK.to_bytes(4, byteorder="big"), addr)

print("file Name = " + file_name)
print("file Size = " + str(file_size))
print("File Path = ./received_dir/" + file_name)

file = open("./received_dir/" + file_name, "wb")

count_size = 0	#while문을 돌리기 위한 조건으로 사용

i = 0

while count_size < file_size:
	i += 1
	
	data, addr = server_sock.recvfrom(1045)	#1045바이트를 전송 받는다
	
	if i == 3:	#timeout 실허험을 위해서 sleep
		time.sleep(5)
		print(" Wait for 5...")
	if i == 9:
		time.sleep(5)
		print(" Wait for 5...")
		
	checksum = data[0:20]	#앞의 20바이트는 checksum
	unhash_data = data[20:]	#뒤의 1025바이트는 seq_num + 데이터
	seq_num = struct.unpack("!b", data[20:21])[0]
	file_data = data[21:]	#seq_num을 제외한 데이터

	hashing_data = hashlib.sha1()
	hashing_data.update(unhash_data)
	hashed_data = hashing_data.digest()	#뒤의 1025바이트를 hash화 시킨다
	if(checksum == hashed_data):	#checksum과 hash화 시킨 것이 같은 경우
		if(seq_num == ACK):
			file.write(file_data)	#파일을 써주고
			ACK = (ACK + 1) % 2	#ACK의 값을 변경
			count_size = count_size + len(file_data)
			size_msg = '( current size / total size ) = ' + str(count_size) + '/' + str(file_size) + ' , ' + str(round((count_size/ file_size), 5)*100) + '%'
			print(size_msg)	#진행률 출력
		
		server_sock.sendto(ACK.to_bytes(4, byteorder="big"), addr)	#sender에게 ACK를 보냄

	else:
		print(" * Packet corrupted!! *** - Send To Sender NAK(2)")
		NAK = 2
		server_sock.sendto(NAK.to_bytes(4, byteorder="big"), addr)

print("File Received End.")

