import sys

import cv2 as cv

# 비디오 파일 열기
cap = cv.VideoCapture('./videos/static.mp4')

if not cap.isOpened():
    print('Video open failed!')
    sys.exit()

# 배경 차분 알고리즘 객체 생성
bs = cv.createBackgroundSubtractorMOG2()
#bs = cv.createBackgroundSubtractorKNN() # 배경영상이 업데이트 되는 형태가 다름
# bs.setDetectShadows(False) # 그림자 검출 안하면 0과 255로 구성된 마스크 출력

# 비디오 매 프레임 처리
while True:
    ret, frame = cap.read()

    if not ret:
        break


    # 0또는 128또는 255로 구성된 fgmask 생성
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    fgmask = bs.apply(gray)
    # fgmask = bs.apply(frame)
    # 배경 영상 받아오기
    back = bs.getBackgroundImage()

    # 레이블링을 이용하여 바운딩 박스 표시
    cnt, _, stats, _ = cv.connectedComponentsWithStats(fgmask)

    for i in range(1, cnt):
        x, y, w, h, s = stats[i]

        if s < 250:
            continue

        cv.rectangle(frame, (x, y, w, h), (0, 0, 255), 2)

    cv.imshow('frame', frame)
    cv.imshow('back', back)
    cv.imshow('fgmask', fgmask)

    if cv.waitKey(20) == 27:
        break

cap.release()
cv.destroyAllWindows()