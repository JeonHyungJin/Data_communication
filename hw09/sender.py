#sender
import socket
import hashlib
import os
import struct
import time

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

window = []	#Window
window_size = 4	#Window 사이즈 4

def make_seq_ack(a, b):
	a = a << 4
	return ((a|b).to_bytes(1, "big"))

def find_ack(a):
	temp_arr = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
	for i in temp_arr:
		if(a == temp_arr[i]):
			return i

seq_num_arr = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]		#seq_num은 0~7 사용
ACK_arr = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
file_send_clear = False

sender_index = 0

print("Sender Socket open..")
print("Receiver IP = " + serverIP)
print("Receiver port = " + str(serverPort))

file_name = input("Input your Message : ")
print("Send File Info(file name, file Size, seqNum) to Server...")
print("Start File send")


file_size = os.path.getsize(file_name)
first_data = file_size.to_bytes(4, byteorder = "big") + file_name.encode()
first_uncheck_msg = make_seq_ack(seq_num_arr[sender_index],ACK_arr[sender_index]) + first_data
file_info_checksum = hashlib.sha1()
file_info_checksum.update(first_uncheck_msg)
file_info_checksum_hashed = file_info_checksum.digest()
msg = file_info_checksum_hashed + first_uncheck_msg

file = open(file_name, "rb")

'''
window.append(msg)
temp_index = sender_index
sender_index = ( sender_index + 1 ) % 8
'''

while not file_send_clear:
	if (len(window) <= window_size) and not file_send_clear:
		
		window.append(msg)
		temp_index = sender_index
		sender_index = ( sender_index + 1 ) % 8

		clnt_sock.sendto(window[0],(serverIP, serverPort))
		data = file.read(1024)
		
		data_msg = make_seq_ack(seq_num_arr[sender_index],ACK_arr[sender_index])+ data
		checksum = hashlib.sha1()	
		checksum.update(data_msg)
		checksum_data = checksum.digest()
		msg = checksum_data + data_msg

	if(not data):
		file_send_clear = True
		break

	recv_ack = clnt_sock.recv(1)
	temp = struct.unpack("!1c",recv_ack)[0]
	ack_num = temp[0] & 0x0F		
	
	finded_ack_index = find_ack(ack_num)
	between_finded_temp_index = abs(finded_ack_index - temp_index)
	
	loop_index = between_finded_temp_index + 1

	for i in range(0, loop_index):
		del window[0]
			


print("File Send End.")
file.close()


