import socket
import struct
import re

use_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

#bytes를 Mac Adress형식으로 바꿔주는 함수
def convertBytesToMacAddr(bytes_addr):
	mac_addr = ""
	splitedStr = re.findall('..', bytes_addr)

	for i in range(0, len(splitedStr)):
		mac_addr += splitedStr[i]
		if i < len(splitedStr) - 1:
			mac_addr += ":"
	return mac_addr

while True:
	packet = use_socket.recvfrom(4096)
	
	ethernet_header = struct.unpack('!6s6s2s', packet[0][0:14])
	dst_ethernet_addr = ethernet_header[0].hex()
	src_ethernet_addr = ethernet_header[1].hex()
	protocol_type = "0x"+ethernet_header[2].hex()
	
	print("201402420전형진\n")
	print("============================================")
	print("                 Ethernet II")
	print("============================================\n")
	print("destination : " + convertBytesToMacAddr(dst_ethernet_addr))
	print("source : " + convertBytesToMacAddr(src_ethernet_addr))
	print("protocol : ",protocol_type)
	print("\n============================================")
	print("                 IPv4")
	print("============================================\n")

#각 정보들을 필요한 Bytes만큼 씩 unpack해준다.
	IPv4_header = struct.unpack('!1s1s2s2s2s1s1s2s4s4s',packet[0][14:34])
	
	version_IP_header_length = IPv4_header[0]
#1바이트로 unpack을 한 정보중 앞의 4bits만 Version에 관한 정보 이므로 비트 연산자를 이용해서 Version부분만을  알아낸다.
	version_bin = version_IP_header_length[0] & 11110000
	version = version_bin >> 4
	print("Version : ", version)
#Version부분이 아닌 bits들이 Header Length부분 이므로 비트 연산자를 이용해서 알아낸다.
	temp_IP_header_length = version_IP_header_length[0] & 15
	IP_header_length = temp_IP_header_length * 4 #Length는 Word단위이므로 1Word는 4Byte이므로 4를곱한다.
	print("Internet Header Length : ", IP_header_length)
#16진수를 10진수로 바꿔서 TOS부분을 출력해준다.
	TOS = int(IPv4_header[1].hex(),16)
	print("TOS : ",TOS)
#TOS와 같은 방식으로 total_length를 출력
	total_Length_hex = IPv4_header[2].hex()
	total_Length =int(total_Length_hex,16)
	print("Total length : ", total_Length)
#TOS와 같은 방식으로 Identification을 출력
	Identification_hex = IPv4_header[3].hex()
	Identification = int(Identification_hex,16)
	print("Identification : ",Identification)
#Flags와 FragmentOffset은 2Bytes에 저장이 되어있고 그중 앞의 3bit만 Flags부분 이므로 비트 연산자를 이용해서 정보를 산출한다.(보고서에 자세한 방법 기술)
	Flags_FragmentOffset = IPv4_header[4]

	temp_Flags = Flags_FragmentOffset[0] & 11100000
	Flags = temp_Flags >> 5
	print("Flags : ", Flags)
#FragmentOffset을 출력한다.(보고서에 자세한 방법 기술)
	temp_Fragment_Offset = Flags_FragmentOffset[0]
	Fragment_Offset = temp_Fragment_Offset << 8
	Fragment_Offset = Fragment_Offset | Flags_FragmentOffset[1]
	Final_Fragment_Offset = Fragment_Offset & 8191
	print("Fragment offset : ", Final_Fragment_Offset)
#TOS와 같은 방식으로 Time to live를 출력
	Time_To_Live = int(IPv4_header[5].hex(), 16)
	print("TTL : ", Time_To_Live)
#TOS와 같은 방식으로 protocol을 출력
	Protocol = int(IPv4_header[6].hex(), 16)
	print("Protocol : ", Protocol)
#TOS와 같은 방식으로 Header_Checksum을 출력
	Header_Checksum = int(IPv4_header[7].hex(), 16)
	print("Header Checksum : ", Header_Checksum)
#socket모듈의 함수를 이용해서 Bytes를 IP주소 형식으로 출력한다.
	Source_Address = socket.inet_ntoa(IPv4_header[8])
	print("Source IP address : " + Source_Address)
#socket모듈의 함수를 이용해서 Bytes를 IP주소 형식으로 출력한다.
	Destination_Address = socket.inet_ntoa(IPv4_header[9])
	print("Destination IP address : " + Destination_Address)

	break
