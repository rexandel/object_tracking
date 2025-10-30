import cv2
import sys
from time import time
import kcf_tracker


ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0
mouse_pressed = False


def draw_boundingbox(event, x, y, flags, param):
    global ix, iy, cx, cy, w, h, mouse_pressed
    
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        ix, iy = x, y
        cx, cy = x, y
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed:
            cx, cy = x, y
    
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        if abs(x-ix) > 10 and abs(y-iy) > 10:
            w, h = abs(x - ix), abs(y - iy)
            ix, iy = min(x, ix), min(y, iy)


if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        cap = cv2.VideoCapture(0)
        interval = 1
    elif len(sys.argv) == 2:
        if sys.argv[1].isdigit():
            cap = cv2.VideoCapture(int(sys.argv[1]))
            interval = 1
        else:
            cap = cv2.VideoCapture(sys.argv[1])
            interval = 30  
    else:  
        sys.exit("too many arguments")

    tracker = None
    cv2.namedWindow('tracking')
    cv2.setMouseCallback('tracking', draw_boundingbox)

    ret, first_frame = cap.read()
    if not ret:
        sys.exit("Failed to read video")

    current_frame = first_frame.copy()
    paused = True

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            current_frame = frame.copy()
        else:
            frame = current_frame.copy()

        if paused and tracker is None:
            display_frame = frame.copy()
            

            if mouse_pressed:
                cv2.rectangle(display_frame, (ix, iy), (cx, cy), (0, 255, 0), 2)
                
            elif w > 0 and h > 0:
                ix_int, iy_int, w_int, h_int = int(ix), int(iy), int(w), int(h)
                cv2.rectangle(display_frame, (ix_int, iy_int), 
                             (ix_int + w_int, iy_int + h_int), (0, 255, 0), 2)
            
            cv2.imshow('tracking', display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                if w > 0 and h > 0:
                    paused = False
                    tracker = kcf_tracker.KCFTracker()
                    ix_int, iy_int, w_int, h_int = int(ix), int(iy), int(w), int(h)
                    tracker.init([ix_int, iy_int, w_int, h_int], frame)
            elif key == 27 or key == ord('q'):
                break
            continue

        if tracker is not None:
            duration = 0.01
            t0 = time()
            boundingbox = tracker.update(frame)
            t1 = time()

            boundingbox = list(map(int, boundingbox))
            x, y, w_track, h_track = boundingbox
            cv2.rectangle(frame, (x, y), (x + w_track, y + h_track), (0, 255, 0), 2)
            
            duration = 0.8 * duration + 0.2 * (t1 - t0)
            fps = 1 / duration if duration > 0 else 0
            cv2.putText(frame, f'FPS: {fps:.1f}', (8, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow('tracking', frame)
        

        c = cv2.waitKey(interval) & 0xFF
        if c == 27 or c == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
