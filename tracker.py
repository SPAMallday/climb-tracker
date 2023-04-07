# openCV 테스트 파일
import numpy as np
import cv2 as cv

cap = cv.VideoCapture('./videos/dyno_s.mp4')

# 비디오 저장용 코덱 설정
fourcc = cv.VideoWriter_fourcc('m','p','4','v')
'''
# 비디오 저장 객체 선언
영상 크기를 읽어오기 위해서 첫 프레임을 임시로 읽어서 크기를 설정함
cv.VideoWriter(저장 파일명, fourcc 코덱, 프레임 수, (가로 크기, 세로 크기))

note :
지금은 30프레임으로 고정이지만 휴대폰 영상 촬영은 프레임 선택이 가능해서 가변적으로 입력 받아야 함
'''

'''
1프레임 확대 확인용으로 사용한 코드 (키보드 입력까지 창 종료 대기)
cv.imshow('frame', frame1)
cv.waitKey(0)
'''

_, frame1 = cap.read()

#TODO 1. 각 배열의 의미는 알겠는데 왜 크기가 생각과 반대로 나오는지?
#TODO 2. 윈도우 속성으로 보는 너비와 높이랑 다른 이유?
#TODO 3. 역으로 뒤집어서 1080x1920 사이즈로 저장하면 카톡 비디오 압축 시 왜 다르게 인식하는지?

height = len(frame1)
width = len(frame1[0])

# 크기 확인
print(f"width : {width}, height : {height}")

out = cv.VideoWriter('output.mp4', fourcc, 30.0, (width,  height))

# 영상 재생 및 저장
while cap.isOpened():
    # 프레임 읽기
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 파일에 쓰기
    out.write(frame)
    # 화면 출력
    cv.imshow('frame', frame)
    # 읽기 완료
    if cv.waitKey(1) == ord('q'):
        break

# 사용한 객체 메모리 반환
cap.release()
out.release()

# 창 모두 닫기
cv.destroyAllWindows()