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


class Winamp():
    """Reader for winamp."""
    def __init__(self):
        self.song = None
        self.attributes = None
        self.window_title = None
        self.previous_title = None

    def read_window_title(self):
        """Find the winamp window title."""
        window_titles = get_titles()
        try:
            winamp = [title for title in window_titles
                      if re.match(r".* Winamp(?: \[.+\])?", title)][0]
        except IndexError:
            winamp = None
        self.previous_title = self.window_title
        self.window_title = winamp

    def song_attributes(self) -> (str, str, str):
        """Parse the song information / status from the winamp title."""
        match = re.match(r"^(\d)+\. (.+) - (.+) - Winamp(?: \[(.+)\])?$",
                         self.window_title)
        author = match.group(2)
        title = match.group(3)
        status = match.group(4)
        return author, title, status

    def refresh(self):
        """Update the view."""
        self.read_window_title()

    def changed(self):
        """Whether the song has changed."""
        return self.previous_title != self.window_title


class Foobar2000():
    """Reader for Foobar2000. NOT IMPLEMENTED YET"""
    def __init__(self, title_template):
        self.song = None
        self.attributes = None
        self.window_title = None
        self.previous_title = None
        self.template = title_template

    def read_window_title(self):
        """Find the foobar window title."""
        window_titles = get_titles()
        try:
            foobar = [title for title in window_titles
                      if title.endswith("[foobar2000]")
                      or title.startswith("foobar2000")][0]
        except IndexError:
            foobar = None
        self.previous_title = self.window_title
        self.window_title = foobar

    def song_attributes(self) -> (str, str, str):
        """Parse the song information from the foobar title."""
        pattern = self.template

        # Place capture groups for watched tags, just match others.
        for tag in re.findall("%.+?%", pattern):
            if tag == r"%title%":
                pattern = pattern.replace(tag, r"(?P<title>.+?)")
                # pattern = pattern.replace(tag, r"(.+?)")
            elif tag == r"%album artist%":
                pattern = pattern.replace(tag, r"(?P<artist>.+?)")
                # pattern = pattern.replace(tag, r"(.+?)")
            else:
                pattern = pattern.replace(tag, ".+?")

        # Replace text-brackets with hex-escape code so they won't be
        # considered int he following
        pattern = re.sub(r"'\['", r"\\x5b", pattern)
        pattern = re.sub(r"'\]'", r"\\x5d", pattern)

        # Remove the quotes around literal strings
        pattern = re.sub(r"'([^']+?)'", r"\1", pattern)

        # Translate foobar optionals to regex optionals
        prev = None
        while pattern != prev:
            prev = pattern
            pattern = re.sub(r"\[([^\[\]]+)\]", r"(?:\1)?", pattern)

        # Excape forwardslashes
        pattern = re.sub(r"([\/])", r"\\\1", pattern)

        # append foobar name to the end of the title
        pattern += r"  \[foobar2000\]"

        # Force the pattern to match from the beginning to the end
        pattern = "^" + pattern + "$"

        match = re.match(pattern, self.window_title)
        if match is None:
            return None, None, "Stopped"
        author = match.group("artist")
        title = match.group("title")
        status = None  # Apparently foobar does not publish this
        return author, title, status

    def refresh(self):
        """Update the view."""
        self.read_window_title()

    def changed(self):
        """Whether the song has changed."""
        return self.previous_title != self.window_title


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


def read_config():
    """Read the config file and setup objects."""
    config = {}
    try:
        with open("config.txt", "r") as file:
            for line in file.readlines():
                if not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    config[key] = value
        if config["player"].casefold() == "winamp":
            player = Winamp()
        elif config["player"].casefold() in ("foobar", "foobar2000"):
            player = Foobar2000(config["foobar title"])
        else:
            raise LookupError(f"Player {config['player']} not supported!")
    except KeyError as err:
        raise KeyError("Malformed config file!") from err
    except FileNotFoundError:
        print("No config file, assuming Winamp.")
        player = Winamp()
    return player


def main():
    """Continuously check for current song."""
    print("Starting program...")
    player = read_config()
    while True:
        try:
            player.refresh()
            if player.changed() and player.window_title is not None:
                author, title, status = player.song_attributes()
                text = ""
                if status not in ["Stopped", "Paused"]:
                    text = find_license(title)
                    print(f"Now displaying {title} by {author}.")
                    if text == "":
                        print("No license found for this song!")
                else:
                    print("Paused or stopped, removing text.")
                edit_file(text)
            time.sleep(1)
        except KeyboardInterrupt:
            input("Goodbye!")
            break


if __name__ == '__main__':
    main()
