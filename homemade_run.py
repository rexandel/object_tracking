import cv2
import os
from time import time
from utils import VideoFileManager
from homemade_kcf import KCFTrackerHomemade


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


def process_video_with_homemade_kcf(video_path, output_dir):   
    global ix, iy, cx, cy, w, h, mouse_pressed
    
    ix, iy, cx, cy = -1, -1, -1, -1
    w, h = 0, 0
    mouse_pressed = False
    
    cap = cv2.VideoCapture(video_path)
    interval = 30

    tracker = None
    cv2.namedWindow('tracking')
    cv2.setMouseCallback('tracking', draw_boundingbox)

    ret, first_frame = cap.read()
    if not ret:
        print(f"Failed to read video: {video_path}")
        return None

    current_frame = first_frame.copy()
    paused = True
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    video_filename = os.path.basename(video_path)
    name_without_ext = os.path.splitext(video_filename)[0]
    output_filename = os.path.join(output_dir, f"{name_without_ext}_homemade_kcf.avi")
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
    
    recording = False
    success = True

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
                    tracker = KCFTrackerHomemade()
                    ix_int, iy_int, w_int, h_int = int(ix), int(iy), int(w), int(h)
                    tracker.init([ix_int, iy_int, w_int, h_int], frame)
                    recording = True
            elif key == 27 or key == ord('q'):
                success = False
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
            fps_display = 1 / duration if duration > 0 else 0
            cv2.putText(frame, f'FPS: {fps_display:.1f}', (8, 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        if recording:
            out.write(frame)

        cv2.imshow('tracking', frame)

        c = cv2.waitKey(interval) & 0xFF
        if c == 27 or c == ord('q'):
            success = False
            break

    cap.release()
    if recording:
        out.release()
        if success:
            print(f"Video saved to: {output_filename}")
    
    cv2.destroyAllWindows()
    
    return output_filename if success else None


def main():
    input_videos_dir = "videos"
    output_base_dir = "tracking_results"
    tracker_name = "homemade_kcf"

    video_files = VideoFileManager.get_video_files(input_videos_dir)
    if not video_files:
        print(f"No video files found in {input_videos_dir}")
        return
    
    VideoFileManager.print_video_list(video_files)
    
    output_dir = VideoFileManager.create_tracker_output_dir(output_base_dir, tracker_name)
    
    print(f"\n{'='*50}")
    print(f"Processing with HOMEMADE KCF tracker")
    print(f"{'='*50}")
    
    successful_processed = []
    
    for i, video_path in enumerate(video_files, 1):
        print(f"\nProcessing video {i}/{len(video_files)}: {os.path.basename(video_path)}")
        
        video_info = VideoFileManager.get_video_info(video_path)
        if video_info:
            print(f"File: {video_info['filename']}, Size: {video_info['size_mb']} MB")
        
        try:
            output_path = process_video_with_homemade_kcf(video_path, output_dir)
            if output_path:
                successful_processed.append(output_path)
                print(f"Successfully processed and saved to: {os.path.basename(output_path)}")
            else:
                print(f"Processing was interrupted by user for: {os.path.basename(video_path)}")
        except Exception as e:
            print(f"Error processing {os.path.basename(video_path)}: {str(e)}")

    print(f"\nCompleted HOMEMADE KCF tracker processing")
    print(f"Results saved to: {output_dir}")
    print(f"Successfully processed {len(successful_processed)}/{len(video_files)} videos")


if __name__ == "__main__":
    main()
