# Tracker APIs (track_trackingAPI.py)

import cv2 as cv

# 트랙커 객체 생성자 함수 리스트 ---①
trackers = [
            # 밝은 배경에 흰옷 회색바지 트래킹 잘 됨, 다이노 추적 불가
            # 좀 빠름
            cv.TrackerMIL_create,
            # 그나마 제일 빠름
            cv.TrackerKCF_create,
            # cv.TrackerGOTURN_create,
            # 유일하게 다이노 추적이 가능한 알고리즘, 밝은 배경에 흰옷 회색바지 트래킹 잘 안될 수 있음
            # 느리지만 위 2가지보다 강한 추적
            cv.TrackerCSRT_create,
            # legacy APIs
            cv.legacy.TrackerBoosting_create,
            cv.legacy.TrackerMedianFlow_create, # 추적이 잘 안됨
            cv.legacy.TrackerMOSSE_create,  # 어느정도 빠르게 추적이 되지만 다이노 불가
            cv.legacy.TrackerTLD_create,    # 너무 튐
            ]
# TODO 중간에 자꾸 놓치는 이유가 뭘까.. 배경색이랑 사람이랑 구분이 힘들어서? -> 객체 외곽선 추출해서 트래킹?

trackerIdx = 0  # 트랙커 생성자 함수 선택 인덱스
tracker = None
isFirst = True

# 비디오 파일과 카메라 선택 ---②
# video_src = "./videos/dyno_s.mp4"
# video_src = "./videos/walk&dyno.mp4"
video_src = "./videos/static.mp4"
cap = cv.VideoCapture(video_src)
fps = cap.get(cv.CAP_PROP_FPS) # 프레임 수 구하기
delay = int(1000/fps)
win_name = 'Tracking APIs'

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print('Cannot read video file')
        break
    img_draw = frame.copy()
    if tracker is None: # 트랙커 생성 안된 경우
        cv.putText(img_draw, "Press the Space to set ROI!!",
                    (100,80), cv.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2,cv.LINE_AA)
    else:
        ok, bbox = tracker.update(frame)   # 새로운 프레임에서 추적 위치 찾기 ---③
        (x,y,w,h) = bbox
        if ok: # 추적 성공
            cv.rectangle(img_draw, (int(x), int(y)), (int(x + w), int(y + h)),
                          (0,255,0), 2, 1)
        else : # 추적 실패
            cv.putText(img_draw, "Tracking fail.", (100,80),
                        cv.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2,cv.LINE_AA)
    trackerName = tracker.__class__.__name__
    cv.putText(img_draw, str(trackerIdx) + ":"+trackerName , (100,20),
                cv.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2,cv.LINE_AA)

    cv.imshow(win_name, img_draw)
    key = cv.waitKey(delay) & 0xff
    # 스페이스 바 또는 비디오 파일 최초 실행 ---④
    if key == ord(' ') or (video_src != 0 and isFirst):
        isFirst = False
        roi = cv.selectROI(win_name, frame, False)  # 초기 객체 위치 설정
        if roi[2] and roi[3]:         # 위치 설정 값 있는 경우
            tracker = trackers[trackerIdx]()    #트랙커 객체 생성 ---⑤
            isInit = tracker.init(frame, roi)
    elif key in range(48, 56): # 0~7 숫자 입력   ---⑥
        trackerIdx = key-48     # 선택한 숫자로 트랙커 인덱스 수정
        if bbox is not None:
            tracker = trackers[trackerIdx]() # 선택한 숫자의 트랙커 객체 생성 ---⑦
            isInit = tracker.init(frame, bbox) # 이전 추적 위치로 추적 위치 초기화
    elif key == 27 :
        break
else:
    print( "Could not open video")
cap.release()
cv.destroyAllWindows()