import cv2
import threading

def capture_screen():
    """Captures the screen and returns a NumPy array."""
    screen = cv2.imread("screen.png")
    return screen

def process_screen(screen):
    """Processes the screen and returns a NumPy array."""
    # Do some processing on the screen, such as blurring or color filtering.
    processed_screen = cv2.blur(screen, (5, 5))
    return processed_screen

def main():
    """Creates a thread to capture the screen and another thread to process the screen."""
    capture_thread = threading.Thread(target=capture_screen)
    process_thread = threading.Thread(target=process_screen)

    # Starts the threads.
    capture_thread.start()
    process_thread.start()

    # Waits for the threads to finish.
    capture_thread.join()
    process_thread.join()

    # Gets the processed screen from the process thread.
    processed_screen = process_thread.result()

    # Displays the processed screen.
    cv2.imshow("Processed Screen", processed_screen)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()
