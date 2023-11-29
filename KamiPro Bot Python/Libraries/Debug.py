from PIL import ImageGrab
import sys
from datetime import datetime
import os

def capture_and_save_screenshot(folder_path="Log"):
    
    # Create the folder if it doesn't exist
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass
    
    try:
        # Capture the screenshot
        screenshot = ImageGrab.grab()

        # Generate a timestamp for the file name
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"screenshot_{timestamp}.png"

        # Save the screenshot to the specified folder and file name
        file_path = os.path.join(folder_path, file_name)
        screenshot.save(file_path)
        print(f"Screenshot saved at: {file_path}")
    except Exception as e:
        print(f"Error capturing and saving screenshot: {e}")


