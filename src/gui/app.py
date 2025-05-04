import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from utils.watermark import add_moving_watermark_with_alpha
from utils.compression import compress_video

class VideoWatermarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Watermarker")

        # Variables
        self.input_video_path = tk.StringVar()
        self.logo_path = tk.StringVar()
        self.output_video_path = tk.StringVar()
        self.scale_value = tk.DoubleVar(value=1.0)
        self.speed_value = tk.DoubleVar(value=1.0)
        self.opacity_value = tk.DoubleVar(value=1.0)
        self.target_size = tk.IntVar(value=10)
        self.quality_value = tk.IntVar(value=28)
        self.should_cancel = False
        self.enable_compression = tk.BooleanVar(value=True)

        # UI setup
        self.create_widgets()

    def create_widgets(self):
        # Input/output section
        self.create_file_selection_section()

        # Settings section
        self.create_settings_section()

        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)

        # Progress label
        self.progress_label = ttk.Label(self.root, text="")
        self.progress_label.pack()

        # Buttons
        self.create_buttons()

        # Branding section
        self.create_branding_section()

    def create_file_selection_section(self):
        frame = ttk.LabelFrame(self.root, text="Files")
        frame.pack(padx=10, pady=10, fill="x")

        self.create_file_selector(frame, "Input Video:", self.input_video_path, 0, filetypes=[("Video files", "*.mp4 *.mov *.avi *.mkv")])
        self.create_file_selector(frame, "Logo (PNG):", self.logo_path, 1, filetypes=[("PNG images", "*.png")])
        self.create_file_selector(frame, "Output Video:", self.output_video_path, 2, is_save=True, filetypes=[("MP4 files", "*.mp4")])


    def create_file_selector(self, parent, label, var, row, is_save=False, filetypes=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        entry = ttk.Entry(parent, textvariable=var, width=50)
        entry.grid(row=row, column=1, padx=5, pady=5)
        action = lambda: self.browse_file(var, is_save, filetypes)
        ttk.Button(parent, text="Browse", command=action).grid(row=row, column=2, padx=5, pady=5)

    def browse_file(self, var, is_save, filetypes):
        if not filetypes:
            filetypes = [("All files", "*.*")]
        if is_save:
            file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=filetypes)
        else:
            file = filedialog.askopenfilename(filetypes=filetypes)
        if file:
            var.set(file)

    def create_settings_section(self):
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.pack(padx=10, pady=10, fill="x")

        self.create_slider(settings_frame, "Scale:", self.scale_value, 0, 0.1, 2.0)
        self.create_slider(settings_frame, "Speed:", self.speed_value, 1, 0.1, 5.0)
        self.create_slider(settings_frame, "Opacity:", self.opacity_value, 2, 0.0, 1.0)

        # Compression Toggle
        ttk.Checkbutton(
            settings_frame,
            text="Enable Compression",
            variable=self.enable_compression,
            command=self.toggle_compression_settings
        ).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        # Target Size
        ttk.Label(settings_frame, text="Target Size (MB):").grid(row=4, column=0, sticky=tk.W)
        self.target_size_scale = ttk.Scale(settings_frame, from_=1, to=100, variable=self.target_size, orient=tk.HORIZONTAL)
        self.target_size_scale.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5)

        # Quality
        ttk.Label(settings_frame, text="Quality (0-51):").grid(row=5, column=0, sticky=tk.W)
        self.quality_scale = ttk.Scale(settings_frame, from_=0, to=51, variable=self.quality_value, orient=tk.HORIZONTAL)
        self.quality_scale.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5)

        # Initially enable/disable based on toggle
        self.toggle_compression_settings()

    def toggle_compression_settings(self):
        state = "normal" if self.enable_compression.get() else "disabled"
        self.target_size_scale.configure(state=state)
        self.quality_scale.configure(state=state)

    def create_slider(self, parent, label, variable, row, min_val, max_val):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W)
        scale = ttk.Scale(parent, from_=min_val, to=max_val, variable=variable, orient=tk.HORIZONTAL)
        scale.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5)

    def create_buttons(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel_processing, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

    def start_processing(self):
        if not all([self.input_video_path.get(), self.logo_path.get(), self.output_video_path.get()]):
            messagebox.showerror("Error", "Please select all required files.")
            return

        self.should_cancel = False
        self.progress["value"] = 0
        self.progress_label.config(text="Starting...")

        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)

        threading.Thread(target=self._process_video_thread).start()

    def cancel_processing(self):
        self.should_cancel = True
        self.progress_label.config(text="Cancelling...")

    def _process_video_thread(self):
        try:
            self.update_progress(10, "Adding watermark...")
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

            if self.enable_compression.get():
                self.update_progress(50, "Compressing video...")
                compress_video(
                    input_video_path="temp_watermarked.mp4",
                    output_video_path=self.output_video_path.get(),
                    target_size_mb=self.target_size.get(),
                    quality=self.quality_value.get()
                )
            else:
                os.rename("temp_watermarked.mp4", self.output_video_path.get())

            self.update_progress(100, "Done!")

        except Exception as e:
            self.progress_label.config(text=f"Error: {str(e)}")
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)

    def update_progress(self, value, text):
        self.progress["value"] = value
        self.progress_label.config(text=text)
        self.root.update_idletasks()

    def create_branding_section(self):
        # Subtle branding at the bottom of the window
        branding_label = ttk.Label(self.root, text="~ By Hari Viapak Garg", font=("Helvetica", 10, "italic"), foreground="gray")
        branding_label.pack(side=tk.BOTTOM, pady=5)
