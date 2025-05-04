import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from utils.watermark import add_moving_watermark_with_alpha
from utils.compression import compress_video
import os

class VideoWatermarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Watermarker - Developed by Hari Viapak Garg")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.input_video_path = tk.StringVar()
        self.logo_path = tk.StringVar()
        self.output_video_path = tk.StringVar()
        self.scale_value = tk.DoubleVar(value=0.08)
        self.opacity_value = tk.DoubleVar(value=0.25)
        self.speed_value = tk.IntVar(value=5)
        self.target_size = tk.DoubleVar(value=10.0)
        self.quality_value = tk.IntVar(value=23)
        self.is_processing = False
        self.should_cancel = False
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create UI components
        self.create_file_selection_section()
        self.create_settings_section()
        self.create_progress_section()
        self.create_button_section()
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
    
    def create_file_selection_section(self):
        # Input Video
        ttk.Label(self.main_frame, text="Input Video:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.input_video_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file("video")).grid(row=0, column=2, padx=5)
        
        # Logo Image
        ttk.Label(self.main_frame, text="Logo Image:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.logo_path, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file("logo")).grid(row=1, column=2, padx=5)
        
        # Output Video
        ttk.Label(self.main_frame, text="Output Video:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.output_video_path, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(self.main_frame, text="Browse", command=lambda: self.browse_file("output")).grid(row=2, column=2, padx=5)
    
    def create_settings_section(self):
        settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Watermark Settings
        ttk.Label(settings_frame, text="Watermark Size:").grid(row=0, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=0.02, to=0.3, variable=self.scale_value, orient=tk.HORIZONTAL).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(settings_frame, text="Opacity:").grid(row=1, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=0.1, to=1.0, variable=self.opacity_value, orient=tk.HORIZONTAL).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(settings_frame, text="Speed:").grid(row=2, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=1, to=20, variable=self.speed_value, orient=tk.HORIZONTAL).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Compression Settings
        ttk.Label(settings_frame, text="Target Size (MB):").grid(row=3, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=1, to=100, variable=self.target_size, orient=tk.HORIZONTAL).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Label(settings_frame, text="Quality (0-51):").grid(row=4, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=0, to=51, variable=self.quality_value, orient=tk.HORIZONTAL).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5)
        
        settings_frame.columnconfigure(1, weight=1)
    
    def create_progress_section(self):
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Progress", padding="10")
        self.progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(self.progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        self.progress_frame.columnconfigure(0, weight=1)
    
    def create_button_section(self):
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.process_button = ttk.Button(
            self.button_frame,
            text="Process Video",
            command=self.process_video
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            self.button_frame,
            text="Cancel",
            command=self.cancel_processing,
            state='disabled'
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
    
    def browse_file(self, file_type):
        if file_type == "video":
            file_path = filedialog.askopenfilename(
                filetypes=[("Video files", "*.mp4 *.avi *.mov")]
            )
            if file_path:
                self.input_video_path.set(file_path)
                # Set default output path
                output_path = os.path.splitext(file_path)[0] + "_watermarked.mp4"
                self.output_video_path.set(output_path)
        elif file_type == "logo":
            file_path = filedialog.askopenfilename(
                filetypes=[("Image files", "*.png *.jpg *.jpeg")]
            )
            if file_path:
                self.logo_path.set(file_path)
        elif file_type == "output":
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4")]
            )
            if file_path:
                self.output_video_path.set(file_path)
    
    def update_progress(self, value, message):
        self.progress_bar['value'] = value
        self.status_label['text'] = message
        self.root.update_idletasks()
    
    def cancel_processing(self):
        if self.is_processing:
            self.should_cancel = True
            self.cancel_button['state'] = 'disabled'
            self.update_progress(0, "Cancelling...")
    
    def process_video(self):
        # Validate inputs
        if not self.input_video_path.get():
            messagebox.showerror("Error", "Please select an input video")
            return
        if not self.logo_path.get():
            messagebox.showerror("Error", "Please select a logo image")
            return
        if not self.output_video_path.get():
            messagebox.showerror("Error", "Please select an output video path")
            return
        
        # Reset cancel flag
        self.should_cancel = False
        
        # Disable process button and enable cancel button
        self.process_button['state'] = 'disabled'
        self.cancel_button['state'] = 'normal'
        self.is_processing = True
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_video_thread)
        thread.start()
    
    # def _process_video_thread(self):
    #     try:
    #         # First add watermark
    #         self.update_progress(0, "Adding watermark...")
    #         if self.should_cancel:
    #             raise Exception("Processing cancelled by user")
            
    #         add_moving_watermark_with_alpha(
    #             input_video_path=self.input_video_path.get(),
    #             logo_path=self.logo_path.get(),
    #             output_video_path="temp_watermarked.mp4",
    #             speed=self.speed_value.get(),
    #             scale=self.scale_value.get(),
    #             opacity=self.opacity_value.get()
    #         )
            
    #         if self.should_cancel:
    #             raise Exception("Processing cancelled by user")
            
    #         # Then compress
    #         self.update_progress(50, "Compressing video...")
    #         compress_video(
    #             input_video_path="temp_watermarked.mp4",
    #             output_video_path=self.output_video_path.get(),
    #             target_size_mb=self.target_size.get(),
    #             quality=self.quality_value.get()
    #         )
            
    #         # Clean up temp file
    #         if os.path.exists("temp_watermarked.mp4"):
    #             os.remove("temp_watermarked.mp4")
            
    #         if not self.should_cancel:
    #             self.update_progress(100, "Processing complete!")
    #             messagebox.showinfo("Success", "Video processing completed successfully!")
        
    #     except Exception as e:
    #         if str(e) == "Processing cancelled by user":
    #             self.update_progress(0, "Processing cancelled")
    #             messagebox.showinfo("Cancelled", "Video processing was cancelled")
    #         else:
    #             messagebox.showerror("Error", f"An error occurred: {str(e)}")
    #             self.update_progress(0, "Error occurred")
        
    #     finally:
    #         self.process_button['state'] = 'normal'
    #         self.cancel_button['state'] = 'disabled'
    #         self.is_processing = False
    #         self.should_cancel = False 

    def _process_video_thread(self):
        try:
            self.update_progress(0, "Adding watermark...")
            if self.should_cancel:
                raise Exception("Processing cancelled by user")
            
            add_moving_watermark_with_alpha(
                input_video_path=self.input_video_path.get(),
                logo_path=self.logo_path.get(),
                output_video_path="temp_watermarked.mp4",
                speed=self.speed_value.get(),
                scale=self.scale_value.get(),
                opacity=self.opacity_value.get()
            )
            
            if self.should_cancel:
                raise Exception("Processing cancelled by user")
            
            self.update_progress(50, "Compressing video...")
            compress_video(
                input_video_path="temp_watermarked.mp4",
                output_video_path=self.output_video_path.get(),
                target_size_mb=self.target_size.get(),
                quality=self.quality_value.get()
            )
            
            if os.path.exists("temp_watermarked.mp4"):
                os.remove("temp_watermarked.mp4")
            
            if not self.should_cancel:
                self.update_progress(100, "Processing complete!")
                self.root.after(0, lambda: messagebox.showinfo("Success", "Video processing completed successfully!"))

        except Exception as e:
            if str(e) == "Processing cancelled by user":
                self.update_progress(0, "Processing cancelled")
                self.root.after(0, lambda: messagebox.showinfo("Cancelled", "Video processing was cancelled"))
            else:
                self.update_progress(0, "Error occurred")
                self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))

        finally:
            self.root.after(0, self._enable_buttons_after_processing)

    def _enable_buttons_after_processing(self):
        self.process_button['state'] = 'normal'
        self.cancel_button['state'] = 'disabled'
        self.is_processing = False
        self.should_cancel = False
