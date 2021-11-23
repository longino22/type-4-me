import pyautogui
from pynput import keyboard, mouse
from PIL import Image
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

x1, y1, x2, y2 = 0, 0, 0, 0
second_click = False


def set_coordinates(has_run):
    global x1, y1, x2, y2
    if has_run is True:
        x1, y1 = pyautogui.position()
        print(f"First coordinates: {x1}, {y1}")
    else:
        x2, y2 = pyautogui.position()
        print(f"Second coordinates: {x2}, {y2}")


# def get_delta():
#     global x1, y1, x2, y2
#     deltaX = x2 - x1
#     deltaY = y2 - y1
#     print(f"Delta of coordinates: {deltaX}, {deltaY}")


def on_click(x, y, button, pressed):
    global second_click
    try:
        if pressed:
            set_coordinates(True)
        if not pressed:
            set_coordinates(False)
            listener.stop()
    except AttributeError:
        pass


with mouse.Listener(on_click=on_click) as listener:
    listener.join()


def take_screenshot():
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save(r"./test.png")


take_screenshot()


def convert_to_text():
    init_image = Image.open("test.png").convert("L")
    init_image.save("grey.png")
    grey_image = Image.open("grey.png")
    text = pytesseract.image_to_string(grey_image)
    text = text.replace("\n", " ")
    text = text.replace("|", "")
    text = " ".join(text.split())
    print(text)
    return text


def type():
    list_of_chars = list(convert_to_text())
    for char in list_of_chars:
        if char == "?":
            break
        keyboard.Controller().press(char)
        time.sleep(0.1)
    else:
        keyboard.Controller().press(keyboard.Key.space)
        take_screenshot()
        type()


time.sleep(3)
type()
