text = '''
제친구가 게임을 좀 못하거든요?,1,0,100
어짜피 계속 해봤자 저한테 질텐데ㅋ,3,0,100
걔 컴퓨터에 접속해서 게임 지워주세요,5,0,100
그럼 뭐라 못하겠지ㅋㅋ,7,0,80
주소는 1.34.5.6에요,9,0,80
아 맞아 걔가요 이상한거 좋아하더라고요ㅋㅋ,11,0,100
최근에 자기가 보안망을 ASCII형식으로 바꿨다고 자랑하던데ㅋㅋ,13,0,130
도움이 되실려나?,14,0,80
'''
text.split('\n')
lines = text.strip().split('\n')
i=0
for line in lines:
    i+=1
    parts = line.split(',')
    if len(parts) == 4:
        dialogue, id, delay, score = parts
        # print(f"ID: {id}, Dialogue: {dialogue}, Delay: {delay}, Score: {score}")
        print(f'{dialogue},0,{delay},{score}')
        # print(f'{dialogue},{id},{delay},{score}')
print(i)
