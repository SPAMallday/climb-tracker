# openCV 테스트 파일
import numpy as np
import cv2 as cv

cap = cv.VideoCapture('./videos/dyno_s.mp4')
# cap = cv.VideoCapture('./videos/dyno_s_high.mov')

# 비디오 저장용 코덱 설정
fourcc = cv.VideoWriter_fourcc('m','p','4','v')
'''
# 비디오 저장 객체 선언
cv.VideoWriter(저장 파일명, fourcc 코덱, 프레임 수, (가로 크기, 세로 크기))

note :
아마 변환 과정에서 30프레임으로 고정시켜야 할 듯 + 오디오랑 싱크를 맞추기 위해 프레임 신경 쓰기
'''


width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv.CAP_PROP_FPS)

# 크기 확인
print(f"width : {width}, height : {height}, fps : {fps}")

out = cv.VideoWriter('output.mp4', fourcc, 30.0, (int(width), int(height)))

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