import time
import cv2
import threading
from subthread_config import Thread_Config
from screenshots import Screenshot

'''
    Represents a screen capturer that checks the current availability of the capture cards and takes screenshots when called.
'''
class ScreenCapturer:
    available_devices = []
    lock = threading.Lock()

    def __init__(self, status_queue):
        self.status_queue = status_queue

    '''
        Adds the message to queue and sends it to the GUI.
    '''
    def send_message(self, message):
        print(message)
        self.status_queue.put(message)         
    
        '''
        Updates the list of available devices by checking if the capture cards are recognised. If it is recognised, the device's index is appended to the available_devices array.
    '''
    def update_available_devices(self):
        for i in range(20):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                if i not in ScreenCapturer.available_devices:
                    with ScreenCapturer.lock:
                        ScreenCapturer.available_devices.append(i)
                cap.release()
            else:
                if i in ScreenCapturer.available_devices:
                    self.send_message(f"WARNING: Device {i} is no longer detected!")
                    with ScreenCapturer.lock:
                        ScreenCapturer.available_devices.remove(i)
                    
        # self.send_message(f"Successfully updated number of devices. The devices are:\n{ScreenCapturer.available_devices}")
        return

    '''
        Iterates through the list of available devices and captures a screenshot for every device and saves it in a folder.
    '''
    def capture_screenshots(self):

        while Thread_Config.running:
            time.sleep(3)
            self.update_available_devices()
            for i in self.available_devices:
                # Check if ADAM GUI application is still running
                if not Thread_Config.running:
                    break

                # Open the video feed from the USB capture card
                cap = cv2.VideoCapture(i)

                if not cap.isOpened():
                    message = f"Error: Could not open device {i}"
                    self.send_message(message)
                    continue

                # Capture one frame
                ret, frame = cap.read()
                
                if ret:
                    with Screenshot.lock:
                        # Store the previous frame if it exists
                        if i in Screenshot.frames:
                            Screenshot.frames[i]['previous'] = Screenshot.frames[i]['current']
                            Screenshot.frames[i]['current'] = frame
                            Screenshot.frames[i]['processed'] = False
                            print(f"Successfully updated the screenshot frames for Device {i}.")
                        else:
                            # Store the current frame in RAM
                            Screenshot.frames[i] = {
                                'current': frame,
                                'previous': None,
                                'processed': False
                            }
                            print("Screenshot added to Screenshot.frames")
                else:
                    message = f"Error: Could not capture frame from device {i}"
                    self.send_message(message)

                # Release the video capture object
                cap.release()
        print("Screencapturer has ended.")