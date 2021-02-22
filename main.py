from pynput.keyboard import Key, Listener
import pyautogui

test_replacements = {"name": "Evan Jackson", "@@": "evanojackson@icloud.com"}


def on_press(key):
    global typed
    global listening

    #format to char
    key_str = str(key).replace('\'', '')

    #begin the word
    if key_str == macro_start:
        typed = []
        listening = True

    if listening:
        if key_str != macro_start and len(key_str) == 1:
            typed.append(key_str)

        print(typed)
        if key == macro_end:
            candidate = ""
            candidate = candidate.join(typed)
            if candidate != "":
                if candidate in test_replacements.keys():
                    pyautogui.press('backspace', presses=len(candidate) +
                                    3)  # // + word + " "
                    pyautogui.typewrite(test_replacements[candidate])
                    listening = False


macro_start = "#"
macro_end = Key.space
typed = []
listening = False

with Listener(on_press=on_press) as listener:
    listener.join()
