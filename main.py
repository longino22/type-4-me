import pyautogui
from pynput import keyboard, mouse
import PIL.Image
import pytesseract
import time
import tkinter
from tkinter import *
from tkinter import ttk, messagebox

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract"

x1, y1, x2, y2 = 0, 0, 0, 0


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


def set_coordinates(has_run):
    global x1, y1, x2, y2
    if has_run is True:
        x1, y1 = pyautogui.position()
    else:
        x2, y2 = pyautogui.position()


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
root.geometry("800x640")
root.title("type4me")


instructions_label = Label(root, text="To begin, select the\narea you want to record")
instructions_label.pack(side=TOP, pady=(15, 5))

state_label = Label(root, text="NOTHING SELECTED", fg="red")
state_label.pack(side=TOP)

select_button = Button(
    root,
    text="Select area",
    command=lambda: [change_state(), select_area(), update_text()],
)
select_button.pack(side=TOP, pady=(5, 15))


def change_state():
    state_label.config(text="SUCCESSFULLY SELECTED", fg="green")


def update_text():
    recognized_label.config(text=convert_to_text())


separator = ttk.Separator(root, orient="horizontal")
separator.pack(fill="x")


text_label = Label(root, text="Recognized text (click to view full text):")
text_label.pack(side=TOP, pady=(15, 0))


def on_click(e):
    messagebox.showinfo("Recognized text", convert_to_text())


recognized_label = Message(root, text="", width=785, fg="blue")
recognized_label.pack(side=TOP)
recognized_label.bind("<Any-Button>", on_click)

type_button = Button(root, text="Start typig", command=type)
type_button.pack(side=BOTTOM, pady=(0, 15))

root.mainloop()
