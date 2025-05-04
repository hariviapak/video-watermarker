# Video Watermarker

A simple application to add watermarks to videos. Developed by Hari Viapak Garg.

## Project Structure

```
video-watermarker/
├── src/
│   ├── gui/
│   │   └── app.py           # GUI application
│   ├── utils/
│   │   ├── watermark.py     # Watermark processing
│   │   └── compression.py   # Video compression
│   └── main.py              # Application entry point
├── requirements.txt         # Python dependencies
├── add_watermarking.spec   # PyInstaller spec file
└── file_version_info.txt   # Windows version info
```

## Features

- Add moving watermarks to videos
- Customize watermark size, opacity, and speed
- Compress output videos
- Cancel processing at any time
- Simple and intuitive interface

## Requirements

- Python 3.11 or later
- FFmpeg (for video compression)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Building the Executable

### Windows

1. Install Python 3.11
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the executable:
   ```bash
   pyinstaller add_watermarking.spec
   ```
4. The executable will be in the `dist` directory

### Using GitHub Actions

1. Push the code to a GitHub repository
2. The GitHub Actions workflow will automatically build the Windows executable
3. Download the executable from the Actions tab

## Usage

1. Run the executable
2. Select your input video file
3. Select your watermark image (PNG with transparency recommended)
4. Choose output location
5. Adjust settings as needed:
   - Watermark Size: Controls how large the watermark appears
   - Opacity: Controls how transparent the watermark is
   - Speed: Controls how fast the watermark moves
   - Target Size: Controls the output file size
   - Quality: Controls the video quality (lower numbers = better quality)
6. Click "Process Video" to start
7. Click "Cancel" at any time to stop processing

## Notes

- The application will create a standalone executable that can run on any Windows computer
- No installation required
- All dependencies are bundled with the executable
- Processing time depends on video length and computer performance

## Support

For issues or feature requests, please open an issue on the GitHub repository.

## License

This project is licensed under the **MIT License**.  
See [LICENSE](https://github.com/hariviapak/video-watermarker/blob/main/LICENSE) for full text.

**Summary**:  
✔ Free to use, modify, and distribute  
✔ Permits private/commercial use  
✔ Only requires attribution  
❌ No liability/warranty  
