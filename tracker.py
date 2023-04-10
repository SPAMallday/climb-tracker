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
아마 변환과정에서 30프레임으로 고정시켜야 할 듯 + 오디오랑 싱크를 맞추기 위해 프레임 신경 쓰기
'''

#TODO 2. 윈도우 속성으로 보는 너비와 높이랑 다른 이유?
#TODO 3. 역으로 뒤집어서 1080x1920 사이즈로 저장하면 카톡 비디오 압축 시 왜 다르게 인식하는지?
#TODO 5. H.265로 하면 HEVC 처리가 가능하다는데,,
# 아이폰에서도 고효율성 (HEVC) / 높은 호환성 (JPEG/H.264) 두가지로 녹화된다

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