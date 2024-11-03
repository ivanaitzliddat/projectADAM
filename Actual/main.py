from screen_capturer import ScreenCapturer
from gui import ADAM
from config import Config
import threading
import queue
import signal

'''
    Starts the screen capturer.
'''
def start_screen_capturer(save_folder, status_queue):
    ss_object = ScreenCapturer(save_folder, status_queue)
    try:
        ss_object.capture_screenshots()
    except Exception as e:
        print(f"Screen capturer encountered an error: {e}")

'''
    Starts the ADAM GUI application.
'''
def run_ADAM(status_queue):
    app = ADAM(status_queue)
    try:
        app.run()
    except Exception as e:
        print(f"ADAM GUI application encountered an error: {e}")

'''
    Handles the signals that are sent to the script, for example, when pressing the ctrl + c button.
'''
def signal_handler(sig, frame):
    ADAM.close()

if __name__ == "__main__":
    save_folder = "./screenshots"
    status_queue = queue.Queue()

    # Register the signal handler for SIGINT
    signal.signal(signal.SIGINT, signal_handler)

    # Start the screen capturer thread
    screen_capturer_thread = threading.Thread(target=start_screen_capturer, args=(save_folder, status_queue))
    screen_capturer_thread.start()

    try:
        run_ADAM(status_queue)
    finally:
        print("Gracefully shutting down screen capturer...")
        # Stop the screen capturer if the GUI is closed
        Config.running = False
        # Wait for the screen capturer to finish
        screen_capturer_thread.join()

    print("Thank you for using ADAM!")