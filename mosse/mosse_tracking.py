import cv2
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from video_file_manager import VideoFileManager

def track_with_mosse(video_path, output_path):
    """
    Трекинг с использованием встроенного MOSSE трекера из OpenCV
    """
    tracker = cv2.legacy_TrackerMOSSE.create()
    
    cap = cv2.VideoCapture(video_path)
    
    success, frame = cap.read()
    if not success:
        print("Ошибка чтения видео")
        return
    
    bbox = cv2.selectROI("Select Object to Track", frame, False)
    print(f"Выбран bbox: {bbox}")
    
    tracker.init(frame, bbox)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame.shape[1], frame.shape[0]))
    
    print("Начинаем трекинг...")
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        track_success, bbox = tracker.update(frame)
        
        if track_success:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "MOSSE Tracking", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Tracking Failure", (50, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow("MOSSE Tracker", frame)
        out.write(frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Результат сохранен в: {output_path}")

def main():
    res_dir = r"Mosse\mosse_videos"
    os.makedirs(res_dir, exist_ok=True)

    video_files = VideoFileManager.get_video_files(r"videos")
    for i, video_path in enumerate(video_files, 1):
        print("===" * 30)
        print(f"Видео {i}/{len(video_files)}: {os.path.basename(video_path)}")
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(res_dir, f"{video_name}_mosse.mp4")
        track_with_mosse(video_path, output_path)

if __name__ == "__main__":
    main()