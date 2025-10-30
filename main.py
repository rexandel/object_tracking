import os
from utils import VideoFileManager
from cv2_trackers import *


def main():
    input_videos_dir = "videos"
    output_base_dir = "tracking_results"

    video_files = VideoFileManager.get_video_files(input_videos_dir)
    if not video_files:
        print(f"No video files found in {input_videos_dir}")
        return
    
    VideoFileManager.print_video_list(video_files)
    
    trackers = {
        'csrt': CSRTTracker(),
        'kcf': KCFTracker(),
        'mosse': MOSSETracker()
    }
    
    for tracker_name, tracker in trackers.items():
        print(f"\n{'='*50}")
        print(f"Processing with {tracker_name.upper()} tracker")
        print(f"{'='*50}")
        
        output_dir = VideoFileManager.create_tracker_output_dir(output_base_dir, tracker_name)
        
        for i, video_path in enumerate(video_files, 1):
            print(f"\nProcessing video {i}/{len(video_files)}: {os.path.basename(video_path)}")
            
            video_info = VideoFileManager.get_video_info(video_path)
            if video_info:
                print(f"File: {video_info['filename']}, Size: {video_info['size_mb']} MB")
            
            try:
                output_path = VideoFileManager.save_processed_video(
                    tracker, video_path, output_dir, tracker_name
                )
                print(f"Successfully processed and saved to: {os.path.basename(output_path)}")
            except Exception as e:
                print(f"Error processing {os.path.basename(video_path)}: {str(e)}")

        print(f"\nCompleted {tracker_name.upper()} tracker processing")
        print(f"Results saved to: {output_dir}")


if __name__ == "__main__":
    main()
