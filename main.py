import pyautogui
from pynput import keyboard
from PIL import Image
import pytesseract


# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"
# screenshot = pyautogui.screenshot()
# screenshot.save(r"./screenshot.png")

# image = Image.open("screenshot.png")
# text = pytesseract.image_to_string(image)
# print(text)

x1, y1, x2, y2 = 0, 0, 0, 0


def set_coordinates(has_run):
    global x1, y1, x2, y2
    if has_run is True:
        x1, y1 = pyautogui.position()
        print(f"First coordinates: {x1}, {y1}")
    else:
        x2, y2 = pyautogui.position()
        print(f"Second coordinates: {x2}, {y2}")


def get_delta():
    global x1, y1, x2, y2
    deltaX = x2 - x1
    deltaY = y2 - y1
    print(f"Delta of coordinates: {deltaX}, {deltaY}")


def on_press(key):
    try:
        if key.char == "1":
            set_coordinates(True)

        if key.char == "2":
            set_coordinates(False)
            get_delta()

        if key.char == "q" or key.char == "s" or key.char == "e":
            print("Program stopped")
            listener.stop()
    except AttributeError:
        pass


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
