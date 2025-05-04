import subprocess
import os

def compress_video(
    input_video_path: str,
    output_video_path: str,
    target_size_mb: float = 10.0,
    quality: int = 23
):
    """
    Compress video while maintaining quality using FFmpeg.
    
    Args:
        input_video_path: Path to input video
        output_video_path: Path to save compressed video
        target_size_mb: Target file size in MB
        quality: CRF value (0-51, lower is better quality)
    """
    # Get video duration using FFprobe
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
        input_video_path
    ]
    duration = float(subprocess.check_output(cmd).decode('utf-8').strip())
    
    # Calculate target bitrate (in kbps)
    target_bitrate = int((target_size_mb * 8192) / duration)  # 8192 = 8 * 1024 (MB to kbps)
    
    # Use FFmpeg for compression
    cmd = [
        'ffmpeg', '-i', input_video_path,
        '-c:v', 'libx264',  # Use H.264 codec
        '-crf', str(quality),  # Constant Rate Factor (lower = better quality)
        '-preset', 'slow',  # Slower preset = better compression
        '-c:a', 'aac',  # Audio codec
        '-b:a', '128k',  # Audio bitrate
        output_video_path
    ]
    
    try:
        subprocess.run(cmd, check=True)
        final_size_mb = os.path.getsize(output_video_path) / (1024 * 1024)
        print(f"\n✅ Video compressed successfully!")
        print(f"Final file size: {final_size_mb:.2f}MB")
        print(f"Saved to: {output_video_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during compression: {e}") 