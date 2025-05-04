import tkinter as tk
from gui.app import VideoWatermarkerApp

def main():
    root = tk.Tk()
    app = VideoWatermarkerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 