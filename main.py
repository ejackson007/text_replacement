import sqlite3 as sl
import os.path
from pynput.keyboard import Key, Listener
import pyautogui

if not os.path.exists("replacements.db"):
    con = sl.connect("replacements.db")
    sql = 'INSERT INTO REPLACEMENTS (short, replace) values (?, ?)'
    data = [("name", "Evan Jackson"), ("@@", "evanojackson@icloud.com")]
    with con:
        con.execute("""
            CREATE TABLE REPLACEMENTS (
                short TEXT,
                replace TEXT
            );
        """)
        con.executemany(sql, data)

macro_start = "#"
macro_end = Key.space
typed = []
listening = False


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

        #print(typed)
        if key == macro_end:
            candidate = ""
            candidate = candidate.join(typed)
            if candidate != "":
                con = sl.connect("replacements.db")
                with con:
                    replace = con.execute(
                        f"SELECT replace FROM REPLACEMENTS WHERE short='{candidate}'"
                    )
                    pyautogui.press('backspace', presses=len(candidate) +
                                    3)  # // + word + " "
                    #gets returned as a tuple, so we have to extract the first value
                    pyautogui.typewrite([row[0] for row in replace][0])
                    listening = False


with Listener(on_press=on_press) as listener:
    listener.join()
