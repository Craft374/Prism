import time
text = '''
어?,1,0,80
오랜만에 돌아왔네?,2,0,80
나 (친구명)이야,3,0,80
어느 순간부터 오프라인 길래 은퇴라도 한 줄 알았지,4,0,100
해킹하는 법은 기억하지?,5,0,80
까먹었을 수도 있으니 내가 도와줄게,6,0,100
조금 있으면 이 밑에 의뢰받기라는 버튼이 나올 거야,7,0,100
그걸 누르면 자동으로 너 컴퓨터로 접속이 될 거야,8,0,100
왼쪽을 보면 "IP 주소 입력"이라는 부분이 보일 거야,9,0,100
그곳에 "192.52.124.12"를 입력하면 내 서브 컴퓨터로 접속이 될 거야,10.5,0,130
컴퓨터 이름 밑쪽을 보면 "Hacking"이란 버튼이 있어,11,0,130
그걸 누르면 잠시 후 다양한 형태의 퍼즐이 등장할 거야,12,0,100
그걸 풀면 ID와 비밀번호를 알 수 있어,13,0,100
그걸 통해 컴퓨터에 접속해,14,0,80
폴더 열기 버튼을 누르면 컴퓨터의 폴더가 열릴 거야,15,0,100
거기서 Delete_Me.txt를 찾아서 지워,16,0,100
그리고 나에게 완료했다고 보내줘,17,0,100
'''
text.split('\n')
lines = text.strip().split('\n')
print("Starting in 3 seconds...")
time.sleep(3)
ttext = []
delay_list = []
for line in lines:
    parts = line.split(',')
    if len(parts) == 4:
        dialogue, delay, type, height = parts
        ttext.append(dialogue)
        delay_list.append(delay)

for i in range(len(ttext)):
    dialogue = ttext[i]
    try:
        if i + 1 < len(delay_list):
            delay = int(delay_list[i + 1]) - int(delay_list[i])
            if delay <= 0:
                delay = 1
        else:
            delay = 1
    except (ValueError, IndexError):
        delay = 1
    print(f'{dialogue}')
    time.sleep(delay)