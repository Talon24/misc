"""Write currently played track to a file. Only Winamp so far."""

import re
import ctypes
import time
# from pprint import pprint

LICENSE_PATH = r"licenses.txt"
WATCHED_FILE = r"music.txt"


def get_titles() -> list:
    """List of all window names that are currently open."""
    enum_windows = ctypes.windll.user32.EnumWindows
    enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                           ctypes.POINTER(ctypes.c_int),
                                           ctypes.POINTER(ctypes.c_int))
    get_window_text = ctypes.windll.user32.GetWindowTextW
    get_window_text_length = ctypes.windll.user32.GetWindowTextLengthW
    is_window_visible = ctypes.windll.user32.IsWindowVisible

    titles = []

    def foreach_window(hwnd, _l_param):
        if is_window_visible(hwnd):
            length = get_window_text_length(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            get_window_text(hwnd, buff, length + 1)
            titles.append(buff.value)
        return True

    enum_windows(enum_windows_proc(foreach_window), 0)

    return titles


def current_song() -> str:
    """Find the winamp window title."""
    window_titles = get_titles()
    try:
        winamp = [title for title in window_titles
                  if re.match(r".* Winamp(?: \[.+\])?", title)][0]
    except IndexError:
        winamp = None
    return winamp


def song_attributes(window_title: str) -> (str, str, str):
    """Parse the song information / status from the winamp title."""
    match = re.match(r"^(\d)+\. (.+) - (.+) - Winamp(?: \[(.+)\])?$",
                     window_title)
    author = match.group(2)
    title = match.group(3)
    status = match.group(4)
    return author, title, status


def find_license(title: str) -> str:
    """Get the Lines in the license file applicable for the given title."""
    output = ""
    with open(LICENSE_PATH, "r") as file:
        for line in file:
            if line.casefold().startswith(title.casefold()):
                output += line
                output += file.readline()
                output += file.readline()
                break
    return output


def edit_file(text: str):
    """Write a text into the file that Streamlabs watches."""
    with open(WATCHED_FILE, "w") as file:
        file.write(text)


def main():
    """Continuously check for current song."""
    print("Starting program...")
    last_checked = ""
    while True:
        try:
            song = current_song()
            if song != last_checked and song is not None:
                last_checked = song
                author, title, status = song_attributes(song)
                text = ""
                if status not in ["Stopped", "Paused"]:
                    text = find_license(title)
                    print("Paused or stopped, removing text.")
                else:
                    print(f"Now displaying {title} by {author}.")
                edit_file(text)
            time.sleep(1)
        except KeyboardInterrupt:
            input("Goodbye!")
            break


if __name__ == '__main__':
    main()
