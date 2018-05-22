#sender
import socket
import hashlib
import os
import struct

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Sender Socket open..")
print("Receiver IP = " + serverIP)
print("Receiver port = " + str(serverPort))

file_name = input("Input your Message : ")
print("Send File Info(file name, file Size, seqNum) to Server...")
print("Start File send")

seq_num = 0	#sequence_number	0,1을 번갈아 가면서 사용

file_size = os.path.getsize(file_name)

file_info_msg = file_size.to_bytes(4, byteorder = "big") + file_name.encode()
file_info_seq_msg = seq_num.to_bytes(1, byteorder = "big") + file_info_msg
file_info_checksum = hashlib.sha1()
file_info_checksum.update(file_info_seq_msg)
file_info_checksum_hashed = file_info_checksum.digest()
file_info_final = file_info_checksum_hashed + file_info_seq_msg

clnt_sock.sendto(file_info_final,(serverIP, serverPort))

recv_ACK = clnt_sock.recv(4)    #4바이트를 전송받음
recv_ACK_int = struct.unpack("!i", recv_ACK)    #ACK로 받은 메세지 int화

if(((seq_num + 1) % 2) == recv_ACK_int):        #ACK
	seq_num = ((seq_num + 1) % 2)   #값 변경



file = open(file_name, "rb")

count_size = 0	#while문을 돌리기 위한 조건으로 사용

while	count_size < file_size:
	
	data = file.read(1024)	#파일을 1024바이트씩 읽음
	seq_data = seq_num.to_bytes(1, byteorder = "big") + data	#뒷 부분의 정보

	checksum = hashlib.sha1()
	checksum.update(seq_data)
	checksum_byte = checksum.digest()	#hash함수로 암호화

	msg = checksum_byte + seq_num.to_bytes(1, byteorder = "big") + data	#메세지

	clnt_sock.sendto(msg,(serverIP, serverPort))	#데이터 메세지 전송

	size_msg = '( current size / total size ) = ' + str(count_size) + '/' + str(file_size) + ' , ' + str(round((count_size / file_size), 5) * 100) + '%'
	print(size_msg)

	recv_ACK = clnt_sock.recv(4)	#4바이트를 전송받음
	recv_ACK_int = struct.unpack("!i", recv_ACK)	#ACK로 받은 메세지 int화

	if(((seq_num + 1) % 2) == recv_ACK_int):	#ACK가 맞는 경우 
		seq_num = ((seq_num + 1) % 2)	#값 변경

	count_size = count_size + len(data)	#while문을 사용하기 위한 조건으로 사용

size_msg = '( current size / total size ) = ' + str(count_size) + '/' + str(file_size) + ',' + str(round((count_size/ file_size), 5)*100) + '%'
print(size_msg)
print("File Send End.")
