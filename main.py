import pyautogui
from pynput import keyboard, mouse
import PIL.Image
import pytesseract
import time
import tkinter
from tkinter import *

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

x1, y1, x2, y2 = 0, 0, 0, 0


def set_coordinates(has_run):
    global x1, y1, x2, y2
    if has_run is True:
        x1, y1 = pyautogui.position()
        print(f"First coordinates: {x1}, {y1}")
    else:
        x2, y2 = pyautogui.position()
        print(f"Second coordinates: {x2}, {y2}")


def select_area():
    def on_click(x, y, button, pressed):
        global second_click
        try:
            if pressed:
                set_coordinates(True)
            if not pressed:
                set_coordinates(False)
                listener.stop()
                take_screenshot()
        except AttributeError:
            pass

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def take_screenshot():
    screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))
    screenshot.save(r"./test.png")


def convert_to_text():
    init_image = PIL.Image.open("test.png").convert("L")
    init_image.save("grey.png")
    grey_image = PIL.Image.open("grey.png")
    text = pytesseract.image_to_string(grey_image)
    text = text.replace("\n", " ")
    text = text.replace("|", "")
    text = " ".join(text.split())
    print(text)
    return text

def type():
    time.sleep(3)
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


root = tkinter.Tk()
root.geometry("150x150")

select_button = Button(root, text="Select area", command=select_area)
select_button.place(x=75, y=50, anchor=CENTER)

start_button = Button(root, text="Start typing", command=type)
start_button.place(x=75, y=100, anchor=CENTER)
root.mainloop()
