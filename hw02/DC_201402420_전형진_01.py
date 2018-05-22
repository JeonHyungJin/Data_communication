import struct

file = open("studentinfo.txt","rb")
student_list = []	#전체 학생 리스트
number_list = [0,0,0,0,0,0,0,0,0,0,0]	#08학번부터 18학번까지 학번 별 사람수 파악을 위한 배열

print("학생들의 정보는 다음과 같습니다.")
for i in range(45):	#데이터 파싱

	student = {}	#dictionary자료형

	data = file.read(1)
	st1 = struct.unpack("!1b",data)
	
	data2 = file.read(9)
	st2 = data2.decode()

	data3 = file.read(2)
	st3 = struct.unpack("!1h",data3)

	data4 = file.read(4)
	st4 = struct.unpack("!1i",data4)
	print("학번:" + str(st1[0]) + "  이름:" + st2 + "  학점:"+ str(st3[0]) +"  나이:"+str(st4[0]))

	student['number'] = st1[0]
	student['name'] = st2
	student['score'] = st3[0]
	student['age'] = st4[0]
	student_list.append(student)	#학생 정보를 리스트에 저장

print("패킷을 분석한 질문들에 대한 대답")	
aver_age_kim = 0	#김씨성을 가진 사람들의 평균 나이 변수 선언
total_age_kim = 0	#김씨성을 가진 사람들의 나이의 합
kim_count = 0		#김씨성을 가진 사람들의 수

for i in range(45):	#김씨성을 가진 사람들의 나이의 총 합을 구하는 반복문
	tempstu = student_list[i]
	temp_name = tempstu['name']
	
	if temp_name[0] == "김":
		kim_count += 1
		total_age_kim += tempstu['age']

aver_age_kim = total_age_kim / kim_count	#김씨성을 가진 사람들의 평균 나이
print("김씨들의 평균 나이는", aver_age_kim, "살입니다.")
		
most_old_lee = ''	#이씨 성을 가진 사람 중 나이가 가장 많은 사람

for i in range(45):	#이씨 성을 가진 사람들 중 맨 앞의 사람 정보 찾기
	tempstu = student_list[i]
	temp_name = tempstu['name']

	if temp_name[0] == "이":
		most_old_lee = tempstu
		break

for i in range(45):	#그 전의 most_old_lee와 비교 하여 가장 나이가 많은 이씨성 찾기
	tempstu = student_list[i]
	temp_name = tempstu['name']

	if temp_name[0] == "이":
		if tempstu['age'] >= most_old_lee['age']:
			most_old_lee = tempstu	#가장 나이 많은 이씨를 찾아서 바꾼다
print("이씨 성을 가진 사람 중 가장 나이가 많은 사람은 " + most_old_lee['name'] + "이며 나이는", most_old_lee['age'], "살 입니다.")

for i in range(45):	#각 학번 별 사람의 수를 카운트
	tempstu = student_list[i]
	temp_number = tempstu['number']
	
	number_list[temp_number-8] += 1

for i in range(len(number_list)):	#학번 별 사람수 출력
	print(i+8, "학번의 학생 수는 ", number_list[i], "명 입니다.")

file.close()
