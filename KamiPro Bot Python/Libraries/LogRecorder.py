from datetime import datetime
from PIL import ImageGrab
import sys
import os

class MemoryLogger:
    def __init__(self):
        self.logs = []

    def write(self, message):
        self.logs.append(message)

    def save_to_file(self, folder_path="Log"):
        try:
            # Generate a timestamp for the file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"console_log_{timestamp}.txt"

            # Save the logs to a text file
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as file:
                for log in self.logs:
                    file.write(f"{log}\n")
            print(f"Console logs saved at: {file_path}")
        except Exception as e:
            print(f"Error saving console logs to file: {e}")

    def save_console_log_to_file(folder_path):
        try:
            # Generate a timestamp for the file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"console_log_{timestamp}.txt"

            # Save the current console log to a text file
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "w") as file:
                sys.stdout = file
                # Add any console log statements you want to capture here
                print("This is a sample console log.")
        except Exception as e:
            print(f"Error saving console log to file: {e}")
        finally:
            # Restore the standard output to the console
            sys.stdout = sys.__stdout__
    
        print(f"Console log saved at: {file_path}")


    
