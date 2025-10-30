import cv2


class BaseTracker:
    def __init__(self, video_path=None):
        self.tracker = None
        self.is_initialized = False
        self.bbox = None
        self.video_path = video_path
        
    def init(self, frame, bbox):
        self.tracker = self.create_tracker()
        success = self.tracker.init(frame, bbox)
        self.is_initialized = success
        self.bbox = bbox
        return success
    
    def update(self, frame):
        if not self.is_initialized or self.tracker is None:
            return False, None
            
        success, bbox = self.tracker.update(frame)
        self.bbox = bbox if success else None
        return success, bbox
    
    def get_bbox(self):
        return self.bbox

    def reset(self):
        self.tracker = None
        self.is_initialized = False
        self.bbox = None

    def create_tracker(self):
        raise NotImplementedError("Subclasses must implement create_tracker method")

    def track_from_video(self, video_path=None, output_path=None):
        if video_path is None:
            if self.video_path is None:
                print("No video path specified")
                return
            video_path = self.video_path
        
        self.reset()
        
        cap = cv2.VideoCapture(video_path)
        
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to open video: {video_path}")
            return
        
        bbox = cv2.selectROI("Select Object to Track", frame, False)
        cv2.destroyWindow("Select Object to Track")
        
        if not self.init(frame, bbox):
            print("Failed to initialize tracker")
            cap.release()
            return
        
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = cap.get(cv2.CAP_PROP_FPS)
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame.shape[1], frame.shape[0]))
        
        print("Tracker initialized. Press 'q' to exit.")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            success, bbox = self.update(frame)

            if success:
                x, y, w, h = [int(i) for i in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Tracking", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Tracking Lost", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            if output_path:
                out.write(frame)
            
            cv2.imshow(f"{self.__class__.__name__} Tracker", frame)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        
        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()
