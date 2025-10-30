import cv2
import numpy as np


class CSRTTracker:
    def __init__(self, video_path=None):
        self.tracker = None
        self.is_initialized = False
        self.bbox = None
        self.video_path = video_path
        
    def init(self, frame, bbox):
        self.tracker = cv2.legacy.TrackerCSRT_create()
        success = self.tracker.init(frame, bbox)
        self.is_initialized = success
        self.bbox = bbox
        return success
    
    def update(self, frame):
        if not self.is_initialized:
            return False, None
            
        success, bbox = self.tracker.update(frame)
        self.bbox = bbox if success else None
        return success, bbox
    
    def get_bbox(self):
        return self.bbox

    def track_from_video(self, video_path=None):
        if video_path is None:
            if self.video_path is None:
                print("Не указан путь к видеофайлу")
                return
            video_path = self.video_path
        
        cap = cv2.VideoCapture(video_path)
        
        ret, frame = cap.read()
        if not ret:
            print(f"Не удалось открыть видео: {video_path}")
            return
        
        bbox = cv2.selectROI("Select Object to Track", frame, False)
        cv2.destroyWindow("Select Object to Track")
        
        if not self.init(frame, bbox):
            print("Не удалось инициализировать трекер")
            cap.release()
            return
        
        print("Трекер инициализирован. Нажмите 'q' для выхода.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            success, bbox = self.update(frame)

            if success:
                x, y, w, h = [int(i) for i in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Tracking", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Tracking Lost", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.imshow("CSRT Tracker", frame)
            
            # Выход по нажатию 'q'
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    tracker = CSRTTracker()
    tracker.track_from_video(r"C:\Users\rexandel\Documents\GitHub\object_tracking\videos\dribbling_ball.mp4")
