import cv2
import numpy as np

def add_moving_watermark_with_alpha(
    input_video_path: str,
    logo_path: str,
    output_video_path: str,
    speed: int = 5,
    scale: float = 0.08,
    opacity: float = 0.25
):
    """
    Add a moving watermark with alpha channel to a video.
    
    Args:
        input_video_path: Path to input video
        logo_path: Path to watermark image (PNG with transparency recommended)
        output_video_path: Path to save watermarked video
        speed: Speed of watermark movement (pixels per frame)
        scale: Size of watermark relative to video height
        opacity: Opacity of watermark (0.0 to 1.0)
    """

    # Load video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {input_video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # Load logo image with alpha channel
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    if logo is None:
        raise ValueError("Cannot load logo image")

    # Convert to RGBA if not already
    if logo.shape[2] == 3:
        logo = cv2.cvtColor(logo, cv2.COLOR_BGR2BGRA)



    # Resize logo
    speed = int(speed)
    logo_h = int(height * float(scale))
    logo_w = int(logo.shape[1] * (logo_h / logo.shape[0]))
    logo = cv2.resize(logo, (logo_w, logo_h), interpolation=cv2.INTER_AREA)

    # Initial position and direction
    x, y = 0, 0
    dx, dy = speed, speed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Bounce logic
        if x + logo_w >= width or x <= 0:
            dx *= -1
        if y + logo_h >= height or y <= 0:
            dy *= -1

        x += dx
        y += dy

        # Ensure coordinates are within bounds
        x = int(round(max(0, min(x, width - logo_w))))
        y = int(round(max(0, min(y, height - logo_h))))

        # Region of Interest
        roi = frame[y:y+logo_h, x:x+logo_w]

        # Ensure ROI and logo have the same dimensions
        if roi.shape != logo.shape[:2]:
            logo = cv2.resize(logo, (roi.shape[1], roi.shape[0]))

        # Split the logo into color and alpha channels
        logo_bgr = logo[:, :, :3]
        alpha = logo[:, :, 3] / 255.0  # Normalize alpha to 0-1
        alpha = alpha * opacity  # Apply additional opacity

        # Create mask for blending
        mask = alpha.reshape(alpha.shape[0], alpha.shape[1], 1)
        mask = np.repeat(mask, 3, axis=2)

        # Blend logo onto ROI using alpha channel
        blended = roi * (1 - mask) + logo_bgr * mask
        frame[y:y+logo_h, x:x+logo_w] = blended.astype(np.uint8)

        out.write(frame)

    cap.release()
    out.release() 